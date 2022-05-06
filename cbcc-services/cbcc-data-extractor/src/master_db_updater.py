import requests
from requests.exceptions import Timeout
import os
import subprocess

from src.utils.config_reader import ConfigReader

class MasterDBUpdater:
    def __init__(self, config_reader: ConfigReader) -> None:
        self.config_reader = config_reader
        
        ## Read Config values
        self.current_truth_version = self.config_reader.read("database", "current_truth_version")
        self.current_hash = self.config_reader.read("database", "current_hash")
        self.latest_version_endpoint = self.config_reader.read("latest_version_endpoint")
        self.database_directory = self.config_reader.read("database", "master_db_directory")
        self.priconne_cdn_host = self.config_reader.read("priconne_cdn_host")
        self.max_test_amount = self.config_reader.read("database", "max_test_amount")
        self.test_multiplier = self.config_reader.read("database", "test_multiplier")
        
        ## Directory paths
        self.current_dir = os.getcwd()
        self.database_dir_path = os.path.join(self.current_dir, self.database_directory)
        
        if not os.path.exists(self.database_dir_path):
            os.makedirs(self.database_dir_path)
        
    def check_and_update_master_db(self):
        initial_load = not os.path.exists(os.path.join(self.database_dir_path, f'master_{self.current_hash}.db'))
        
        latest_truth_version, latest_hash = self.get_latest_truth_version_and_hash()
            
        if (not initial_load and latest_truth_version == self.current_truth_version):
            print("Current truth version matches the current latest truth version, no master database updates required.")
        else:
            print("New truth version and hash required (or there was no initial load), beginning new master db retrieval")
            self.retrieve_and_decrypt_cdn_master_db(latest_hash)
            
            self.config_reader.write(latest_truth_version, "database", "current_truth_version")
            self.config_reader.write(latest_hash, "database", "current_hash")
            
            print('Updated config with latest truth version and hash')
            

    def get_latest_truth_version_and_hash(self):
        try:
            print("Attempting to hit estertion endpoint")
            latest_version_response = requests.get(self.latest_version_endpoint, timeout=10)
        except Timeout:
            print('Estertion request timed out, beginning the guess and check method')
            latest_truth_version, latest_hash = self.guess_and_check()
        else:
            print("Estertion request successful")
            latest_version_response_json = latest_version_response.json()
            latest_truth_version, latest_hash = latest_version_response_json["TruthVersion"], latest_version_response_json["hash"]
            
        return latest_truth_version, latest_hash

    def guess_and_check(self):
        latest_truth_version, latest_hash = self.current_truth_version, self.current_hash
        
        i = 0
        while i < self.max_test_amount:
            truth_version_guess = int(self.current_truth_version) + (i * int(self.test_multiplier))
            
            asset_manifest_endpoint = f'{self.priconne_cdn_host}/dl/resources/{truth_version_guess}/Jpn/AssetBundles/Windows/manifest/masterdata_assetmanifest'
            masterdata_assetmanifest_response = requests.get(asset_manifest_endpoint)
            
            if (masterdata_assetmanifest_response.ok):
                print('Found new truth version, updating the new truth')
                response_text = masterdata_assetmanifest_response.text
                
                latest_truth_version = truth_version_guess
                latest_hash = response_text.split(',')[1]
                
                break
            
            i += 1
        
        return latest_truth_version, latest_hash

    def retrieve_and_decrypt_cdn_master_db(self, latest_hash):
        cdb_path = os.path.join(self.database_dir_path, 'master.cdb')
        db_path = os.path.join(self.database_dir_path, f'master_{latest_hash}.db')
        
        db_endpoint = f'{self.priconne_cdn_host}/dl/pool/AssetBundles/{latest_hash[0:2]}/{latest_hash}'
        encrypted_db_response = requests.get(db_endpoint)
        
        with open(cdb_path, 'wb') as cdb_file:
            cdb_file.write(encrypted_db_response.content)
            
        coneshell_exe = os.path.join(self.current_dir, 'Coneshell_call.exe')
        coneshell_call = f"{coneshell_exe} -cdb {cdb_path} {db_path}"
        subprocess.run(coneshell_call, shell=True)
        print("new database has been retrieved")
        
        os.remove(cdb_path)
        print("Removed cdb file")