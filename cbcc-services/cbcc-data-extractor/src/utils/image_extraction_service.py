import logging
import os
import pathlib
import requests

from io import BytesIO

import unitypack
from PIL import ImageOps

import struct

class ImageExtractionService:
    def __init__(self, config) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        ## Read Config values
        self.priconne_cdn_host = config["endpoints"]["priconne_cdn_host"]
        self.manifest_directory = config["directories"]["manifest_directory"]
        self.manifest_file = config["pcrddatabase"]["manifest_file"]
        self.temp_assets_directory = config["directories"]["temp_assets_directory"]
        self.unity_assets_directory = config["directories"]["unity_assets_directory"]
        self.deserialized_assets_directory = config["directories"]["deserialized_assets_directory"]
       
        ## Directory paths
        self.current_dir = os.getcwd()
        self.current_unit_manifest_file = os.path.join(self.current_dir, self.manifest_directory, self.manifest_file)
        
        if not os.path.exists(os.path.join(self.current_dir, self.temp_assets_directory)):
            os.makedirs(os.path.join(self.current_dir, self.temp_assets_directory))

        if not os.path.exists(self.current_unit_manifest_file):
            raise FileNotFoundError("The current manifest file could not be found, make sure it's built first")
        
        with open(self.current_unit_manifest_file, 'r') as unit_manifest:
            manifest_lines = unit_manifest.read().splitlines()
        
        self.unit_asset_file_to_hash_map = {x.split(',')[0]:x.split(',')[1] for x in manifest_lines}

    # Returns the directory of where the icon has been deserialized to for further use
    def make_unit_icon(self, unit_name, icon_id, thematic='') -> str:
        icon_dir = self.set_full_unit_name(unit_name, thematic)

        self.logger.info(f'Checking icons for {icon_dir}')

        if self.check_icon_already_exist(icon_dir, icon_id):
            self.logger.warn("Icon have already been made")
            return icon_dir
        
        self.retrieve_unity_asset_for_character(icon_dir, icon_id)
        self.deserialize_unity_asset_into_png(icon_dir)
        
        return icon_dir
    
    def check_icon_already_exist(self, icon_dir, icon_id) -> bool:
        icon_png = f'{icon_dir}_{icon_id}.png'
        unit_converted_pngs_directory = os.path.join(self.current_dir, self.temp_assets_directory, icon_dir, self.deserialized_assets_directory, icon_png)
        
        return os.path.exists(unit_converted_pngs_directory)
    
    def retrieve_unity_asset_for_character(self, icon_dir, icon_id):
        unit_temp_assets_directory = os.path.join(self.current_dir, self.temp_assets_directory, icon_dir, self.unity_assets_directory)
        
        if not os.path.exists(unit_temp_assets_directory):
            os.makedirs(unit_temp_assets_directory)
        
        unit_icon_unity_file_path = os.path.join(unit_temp_assets_directory, f'{icon_dir}_{icon_id}.unity3d')
        unit_icon_unity_file_in_manifest = f'a/unit_icon_unit_{icon_id}.unity3d'
        
        if unit_icon_unity_file_in_manifest in self.unit_asset_file_to_hash_map:
            self.logger.info(f"Retrieving unity file with id: {icon_id}")
            hash = self.unit_asset_file_to_hash_map[unit_icon_unity_file_in_manifest]
            
            icon_endpoint = f'{self.priconne_cdn_host}/dl/pool/AssetBundles/{hash[0:2]}/{hash}'
            self.logger.debug(f'Retrieving the encrypted icon from {icon_endpoint}')
            encrypted_icon_response = requests.get(icon_endpoint)
            
            with open(unit_icon_unity_file_path, 'wb') as unity_file:
                unity_file.write(encrypted_icon_response.content) 
        else:
            self.logger.warn(f'File {unit_icon_unity_file_in_manifest} not found')
    
    
    def deserialize_unity_asset_into_png(self, icon_dir):
        unit_temp_assets_directory = os.path.join(self.current_dir, self.temp_assets_directory, icon_dir, self.unity_assets_directory)
        unit_converted_pngs_directory = os.path.join(self.current_dir, self.temp_assets_directory, icon_dir, self.deserialized_assets_directory)
        
        if not os.path.exists(unit_converted_pngs_directory):
            os.makedirs(unit_converted_pngs_directory)
            
        for unity_filename in os.listdir(unit_temp_assets_directory):
            unity_file_path = os.path.join(unit_temp_assets_directory, unity_filename)
            unity_file_name_without_extension = pathlib.Path(unity_file_path).stem
            png_export_path = os.path.join(unit_converted_pngs_directory, f'{unity_file_name_without_extension}.png')
            
            with open(unity_file_path, 'rb') as unity_3d_file:
                self.run_deserialization_process(unity_3d_file, png_export_path)
                
    
    def run_deserialization_process(self, unity_3d_file, png_export_path):
        try: 
            bundle = unitypack.load(unity_3d_file)
            for asset in bundle.assets:   
                for _, object in asset.objects.items():
                    if object.type == 'Texture2D':
                        data = object.read()
                        try:
                            image = data.image
                        except NotImplementedError:
                            continue
                        if image is None:
                            continue
                        
                        img = ImageOps.flip(image)
                        output = BytesIO()
                        img.save(output, format='png')
                        
                        with open(png_export_path, 'wb') as png_file:
                            png_file.write(output.getvalue())
                            self.logger.info(f"Completed Deserialization for {png_export_path}")
                            return
        except struct.error:
            self.logger.warn('Hit a struct error related to the unity pack library while deserializing')
            return 
        
    def set_full_unit_name(self, unit_name, thematic=''):
        if not thematic:
            return unit_name
        
        return f'{unit_name}_{thematic}'
    
    