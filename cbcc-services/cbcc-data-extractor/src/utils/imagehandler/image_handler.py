import logging
import os
from typing import Tuple

class ImageHandler():
    def __init__(self, image_store, temp_assets_directory, deserialized_assets_directory) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        self.image_store = image_store
        
        # Read Config Values
        self.temp_assets_directory = temp_assets_directory
        self.deserialized_assets_directory = deserialized_assets_directory
        
        ## Directory paths
        self.current_dir = os.getcwd()
    
    def check_image_exists(self, unit_icon_folder_name: str, icon_id: str) -> Tuple[bool, str]:
        image_name = f'{unit_icon_folder_name}_{icon_id}.png'        
        self.logger.info(f'Checking if image: {image_name} is in the image store')
        return self.image_store.retrieve(image_name)
    
    def store_new_icon_images(self, unit_icon_folder_name: str, icon_id: str):
        image_name = f'{unit_icon_folder_name}_{icon_id}.png'
        image_location_on_disk = os.path.join(self.current_dir, self.temp_assets_directory, unit_icon_folder_name,  self.deserialized_assets_directory, image_name)
        
        self.logger.debug(f'Checking if file location {image_location_on_disk} exists')

        if not os.path.exists(image_location_on_disk):
            self.logger.warn(f'Path does not exist, will not attempt to store image {image_name}')
            return
        
        self.logger.info(f'Attempting to store image {image_name}')
        self.image_store.store(image_location_on_disk, image_name)
        return self.image_store.retrieve(image_name)
        