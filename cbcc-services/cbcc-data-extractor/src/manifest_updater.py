import os
import requests

from src.utils.config_reader import ConfigReader

class ManifestUpdater:
    def __init__(self, config_reader: ConfigReader) -> None:
        self.config_reader = config_reader
       
        ## Read Config values
        self.current_truth_version = self.config_reader.read("database", "current_truth_version")
        self.priconne_cdn_host = self.config_reader.read("priconne_cdn_host")
        self.manifest_directory = self.config_reader.read("manifest_directory")
       
        ## Directory paths
        self.current_dir = os.getcwd()
        self.manifest_path = os.path.join(self.current_dir, self.manifest_directory)
        
        if not os.path.exists(self.manifest_path):
            os.makedirs(self.manifest_path)
       
    def get_unit_manifest(self):
        current_unit_manifest_path = os.path.join(self.manifest_path, f'unit_manifest_{self.current_truth_version}.txt')
        if os.path.exists(current_unit_manifest_path):
            print('Already have latest unit manifest')
            return
        
        print('Retrieving latest unit manifest')
        
        unit_manifest_endpoint = f'{self.priconne_cdn_host}/dl/Resources/{self.current_truth_version}/Jpn/AssetBundles/Windows/manifest/unit2_assetmanifest'
        unit_manifest_response = requests.get(unit_manifest_endpoint)
        
        with open(current_unit_manifest_path, 'w') as unit_manifest_file:
            unit_manifest_file.write(unit_manifest_response.text)
            
        print('Retrieved latest unit manifest')