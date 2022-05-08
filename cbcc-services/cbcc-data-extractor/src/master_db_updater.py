import json
import logging
from typing import Tuple
import requests
from requests.exceptions import Timeout
import os
import subprocess

class MasterDBUpdater:
    def __init__(self, config) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        # Configs
        self.latest_version_endpoint = config["endpoints"]["latest_version_endpoint"]
        self.api_version_directory = config["directories"]["api_version_directory"]
        self.api_version = config["pcrddatabase"]["api_version_info"]
        self.database_directory = config["directories"]["master_db_directory"]
        self.master_db = config["pcrddatabase"]["master_db"]
        self.priconne_cdn_host = config["endpoints"]["priconne_cdn_host"]
        
        ## Directory paths
        self.current_dir = os.getcwd()
        self.database_dir_path = os.path.join(self.current_dir, self.database_directory)
        self.api_version_info = os.path.join(self.current_dir, self.api_version_directory)

        if not os.path.exists(self.database_dir_path):
            os.makedirs(self.database_dir_path)

        if not os.path.exists(self.api_version_info):
            os.makedirs(self.api_version_info)


    def get_current_api_version(self, api_version_json) -> Tuple[int, str]:
         with open(api_version_json, 'rb') as api_version_data:
            api_version_data = json.load(api_version_data)
            return int(api_version_data["current_truth_version"]), str(api_version_data["current_hash"])


    def write_current_api_version(self, api_version_json, latest_truth_version, latest_hash):
        api_version_data = { "current_truth_version": latest_truth_version, "current_hash": latest_hash}
        with open(api_version_json, 'w') as api_version_data_file:
            api_version_data_file.write(json.dumps(api_version_data, ensure_ascii=False, indent=4))


    def get_latest_truth_version_and_hash(self):
        try:
            self.logger.info("Attempting to hit estertion endpoint")
            latest_version_response = requests.get(self.latest_version_endpoint, timeout=10)
        except Timeout:
            self.logger.error('Estertion request timed out')
            raise
        
        self.logger.info("Estertion request successful")
        latest_version_response_json = latest_version_response.json()
        latest_truth_version, latest_hash = latest_version_response_json["TruthVersion"], latest_version_response_json["hash"]
            
        return latest_truth_version, latest_hash


    def check_and_update_master_db(self):
        current_truth_version, current_hash = 0, ""
        api_version_json = os.path.join(self.api_version_info, self.api_version)
        if os.path.exists(api_version_json):
            current_truth_version, current_hash = self.get_current_api_version(api_version_json)

        latest_truth_version, latest_hash = self.get_latest_truth_version_and_hash()
            
        if (int(latest_truth_version) == current_truth_version):
            self.logger.info(f"Current truth version {current_truth_version} matches the latest truth version {latest_truth_version}, no master database updates required.")
        else:
            self.logger.info("New truth version and hash found, beginning new master db retrieval")
            self.retrieve_and_decrypt_cdn_master_db(latest_hash)
            self.write_current_api_version(api_version_json, latest_truth_version, latest_hash)
            self.logger.debug('Updated config with latest truth version and hash')


    def retrieve_and_decrypt_cdn_master_db(self, latest_hash):
        cdb_path = os.path.join(self.database_dir_path, 'master.cdb')
        db_path = os.path.join(self.database_dir_path, self.master_db)
        
        db_endpoint = f'{self.priconne_cdn_host}/dl/pool/AssetBundles/{latest_hash[0:2]}/{latest_hash}'

        self.logger.debug(f'Retrieving encrypted database from {db_endpoint}')

        encrypted_db_response = requests.get(db_endpoint)
        
        with open(cdb_path, 'wb') as cdb_file:
            cdb_file.write(encrypted_db_response.content)
            
        coneshell_exe = os.path.join(self.current_dir, 'Coneshell_call.exe')
        coneshell_call = f"{coneshell_exe} -cdb {cdb_path} {db_path}"
        subprocess.run(coneshell_call, shell=True)
        self.logger.debug("new database has been retrieved")
        
        os.remove(cdb_path)
        self.logger.debug("Removed cdb file")