import os
import pathlib
import requests

from io import BytesIO

import unitypack
from PIL import ImageOps

import struct 
from dependency_injector.wiring import Provide

from src.containers import Container
from src.models.unit_id_container import UnitIdContainer

class ImageExtractionService:
    def __init__(self) -> None: 
        ## Read Config values
        self.priconne_cdn_host = Provide[Container.config.endpoints.priconne_cdn_host]
        self.manifest_directory = Provide[Container.config.directories.manifest_directory]
        self.manifest_file = Provide[Container.config.pcrddatabase.manifest_file]
        self.temp_assets_directory = Provide[Container.config.directories.temp_assets_directory]
        self.unity_assets_directory = Provide[Container.config.directories.unity_assets_directory]
        self.deserialized_assets_directory = Provide[Container.config.directories.deserialized_assets_directory]
       
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
        
    def make_unit_icons(self, unit_name, unit_id_container: UnitIdContainer, playable_character=False, thematic='') -> str:
        if self.check_icons_already_exist(unit_name, thematic):
            print("Icons have already been made")
            return self.set_full_unit_name(unit_name, thematic)
        
        if (playable_character):
            self.retrieve_unity_asset_for_character(unit_name, 
                                                    thematic, 
                                                    unit_id_container.one_star_icon_id, 
                                                    unit_id_container.three_star_icon_id, 
                                                    unit_id_container.six_star_icon_id)
            self.deserialize_unity_asset_into_png(unit_name, thematic) 
        else:
            self.retrieve_unity_asset_for_character(unit_name, thematic, unit_id_container.unit_id)
            self.deserialize_unity_asset_into_png(unit_name, thematic)
        
        return self.set_full_unit_name(unit_name, thematic)
    
    def check_icons_already_exist(self, unit_name, thematic='') -> bool:
        full_unit_name = self.set_full_unit_name(unit_name, thematic)
        unit_converted_pngs_directory = os.path.join(self.current_dir, self.temp_assets_directory, full_unit_name, self.deserialized_assets_directory)
        
        return os.path.exists(unit_converted_pngs_directory) and len(os.listdir(unit_converted_pngs_directory)) > 0
    
    def retrieve_unity_asset_for_character(self, unit_name, thematic='', *icon_ids):
        full_unit_name = self.set_full_unit_name(unit_name, thematic)
        unit_temp_assets_directory = os.path.join(self.current_dir, self.temp_assets_directory, full_unit_name, self.unity_assets_directory)
        
        if not os.path.exists(unit_temp_assets_directory):
            os.makedirs(unit_temp_assets_directory)
        
        for icon_id in icon_ids:
            unit_icon_unity_file_path = os.path.join(unit_temp_assets_directory, f'{full_unit_name}_{icon_id}.unity3d')
            unit_icon_unity_file_in_manifest = f'a/unit_icon_unit_{icon_id}.unity3d'
            
            if unit_icon_unity_file_in_manifest in self.unit_asset_file_to_hash_map:
                print(f"Retrieving unity file with id: {icon_id}")
                hash = self.unit_asset_file_to_hash_map[unit_icon_unity_file_in_manifest]
                
                icon_endpoint = f'{self.priconne_cdn_host}/dl/pool/AssetBundles/{hash[0:2]}/{hash}'
                encrypted_icon_response = requests.get(icon_endpoint)
                
                with open(unit_icon_unity_file_path, 'wb') as unity_file:
                    unity_file.write(encrypted_icon_response.content) 
            else:
                print(f'File not found, moving on')
    
    
    def deserialize_unity_asset_into_png(self, unit_name, thematic=''):
        full_unit_name = self.set_full_unit_name(unit_name, thematic)
        unit_temp_assets_directory = os.path.join(self.current_dir, self.temp_assets_directory, full_unit_name, self.unity_assets_directory)
        unit_converted_pngs_directory = os.path.join(self.current_dir, self.temp_assets_directory, full_unit_name, self.deserialized_assets_directory)
        
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
                            print(f"Completed Deserialization for {png_export_path}")
                            return
        except struct.error:
            print('Hit a struct error related to the unity pack library while deserializing')
            return 
        
    def set_full_unit_name(self, unit_name, thematic=''):
        if not thematic:
            return unit_name
        
        return f'{unit_name}_{thematic}'
    
    