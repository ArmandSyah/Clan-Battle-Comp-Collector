import os
from typing import Tuple

from src.utils.config_reader import ConfigReader
from src.utils.imagehandler.imagestore.base_image_store import BaseImageStore

class ImageHandler():
    def __init__(self, config_reader: ConfigReader, image_store: BaseImageStore) -> None:
        self.config_reader = config_reader
        self.image_store = image_store
        
        # Read Config Values
        self.temp_assets_directory = self.config_reader.read("image_extraction", "temp_assets_directory")
        self.deserialized_assets_directory = self.config_reader.read("image_extraction", "deserialized_assets_directory")
        
        ## Directory paths
        self.current_dir = os.getcwd()
    
    def check_image_exists(self, unit_icon_folder_name: str, icon_id: str) -> Tuple[bool, str]:
        image_name = f'{unit_icon_folder_name}_{icon_id}.png'        
        return self.image_store.retrieve(image_name)
    
    def store_new_icon_images(self, unit_icon_folder_name: str, icon_id: str):
        image_name = f'{unit_icon_folder_name}_{icon_id}.png'
        image_location_on_disk = os.path.join(self.current_dir, self.temp_assets_directory, unit_icon_folder_name,  self.deserialized_assets_directory, image_name)
        
        if not os.path.exists(image_location_on_disk):
            print('Path does not exist, will not attempt to store')
            return
        
        self.image_store.store(image_location_on_disk, image_name)
        return self.image_store.retrieve(image_name)
        