import json
import logging
import os
import requests

class ManifestUpdater:
    def __init__(self, config) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        ## Read Config values
        self.api_version_directory = config["directories"]["api_version_directory"]
        self.api_version_info = config["pcrddatabase"]["api_version_info"]
        self.priconne_cdn_host = config["endpoints"]["priconne_cdn_host"]
        self.manifest_directory = config["directories"]["manifest_directory"]
        self.manifest_file = config["pcrddatabase"]["manifest_file"]
       
        ## Directory paths
        self.current_dir = os.getcwd()
        self.manifest_path = os.path.join(self.current_dir, self.manifest_directory)
        self.api_version_path = os.path.join(self.current_dir, self.api_version_directory)
        
        if not os.path.exists(self.manifest_path):
            os.makedirs(self.manifest_path)
        
        # Get the current truth version
        api_version_json = os.path.join(self.api_version_path, self.api_version_info)
        with open(api_version_json, 'rb') as api_version_data:
            api_version_data = json.load(api_version_data)
            self.current_truth_version = api_version_data["current_truth_version"]
       
    def get_unit_manifest(self):
        current_unit_manifest_path = os.path.join(self.manifest_path, self.manifest_file)
        
        self.logger.info('Retrieving latest unit manifest')
        
        unit_manifest_endpoint = f'{self.priconne_cdn_host}/dl/Resources/{self.current_truth_version}/Jpn/AssetBundles/Windows/manifest/unit2_assetmanifest'
        unit_manifest_response = requests.get(unit_manifest_endpoint)
        
        with open(current_unit_manifest_path, 'w') as unit_manifest_file:
            unit_manifest_file.write(unit_manifest_response.text)
            
        self.logger.info('Retrieved latest unit manifest')