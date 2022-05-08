import json
import logging
import os
from src.models.unit_id_container import UnitIdContainer

class PlayableUnitsPipeline:
    def __init__(self, master_db_reader, kakasi, translator, image_extraction_service, image_handler, config) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        self.master_db_reader = master_db_reader
        self.kakasi = kakasi
        self.translator = translator
        self.image_extraction_service = image_extraction_service
        self.image_handler = image_handler
        
        ## Configs
        current_dir = os.getcwd()
        self.pipeline_results_directory = config["directories"]["pipeline_results_directory"]
        self.character_json = config["pipeline_results"]["character"]

        if not os.path.exists(os.path.join(current_dir, self.pipeline_results_directory)):
            os.makedirs(os.path.join(current_dir, self.pipeline_results_directory))
        
        self.current_thematics = dict()
        self.retrieved_unit_ids = set()
        self.character_data = []
        
    
    def retrieve_current_character_info(self):
        character_json_path = os.path.join(os.getcwd(),self.pipeline_results_directory, self.character_json)
        
        if not os.path.exists(character_json_path):
            self.logger.debug('Character.json doesn\'t exist, retrieving fresh character data')
            self.current_thematics = dict()
            self.retrieved_unit_ids = set()
            self.character_data = []
            return
        
        with open(character_json_path, 'rb') as character_json_file:
            try:
                self.character_data = json.load(character_json_file)
                self.retrieved_unit_ids = set(character['unit_id'] for character in self.character_data)    
            except (json.JSONDecodeError):
                self.logger.debug(f'Something went wrong with loading {self.character_json}, retrieving fresh character data')
                self.current_thematics = dict()
                self.retrieved_unit_ids = set()
                self.character_data = []
            
        
    def build_character_json(self):
        self.retrieve_current_character_info()
        
        character_query = '''
                        select unit_id, unit_name, prefab_id, search_area_width, comment
                        from unit_data
                        where unit_id < 190000 and comment <> ''
                        order by search_area_width 
                        '''
        
        character_results = self.master_db_reader.query_master_db(character_query)
        
        for _, character in character_results.iterrows():
            unit_id = character['unit_id']
            
            if unit_id in self.retrieved_unit_ids:
                self.logger.debug(f'Character with unit id {unit_id} has already been processed')
                continue
            
            self.logger.info(f"Processing character {unit_id}: {character['unit_name']}")
            # thematics
            jp_thematic = self.check_unit_thematic(character["unit_name"])
            
            if not jp_thematic in self.current_thematics:
                en_thematic = self.translator.translate(jp_thematic)
                self.current_thematics[jp_thematic] = en_thematic
            else:
                en_thematic = self.current_thematics[jp_thematic]
            
            name = character["unit_name"].split('(')[0]
            # Get the romanized string of the katakana
            romanized_name = self.handle_unit_name(name)
            
            jp_description = character["comment"].replace('\n', '')
            en_description = self.translator.translate(jp_description)
            
            unit_id_container = UnitIdContainer(unit_id, True)
            unit_icon_folder_name = self.image_extraction_service.make_unit_icons(romanized_name, unit_id_container, playable_character=True, thematic=en_thematic)
            
            ### Checking for existance of icons in the image store first
            one_star_icon = self.image_handler.check_image_exists(unit_icon_folder_name, unit_id_container.one_star_icon_id)
            three_star_icon = self.image_handler.check_image_exists(unit_icon_folder_name, unit_id_container.three_star_icon_id)
            six_star_icon = self.image_handler.check_image_exists(unit_icon_folder_name, unit_id_container.six_star_icon_id)
            
            character_icon_locations = {
                'one_star_icon': one_star_icon if one_star_icon is not None else self.image_handler.store_new_icon_images(unit_icon_folder_name, unit_id_container.one_star_icon_id),
                'three_star_icon': three_star_icon if three_star_icon is not None else self.image_handler.store_new_icon_images(unit_icon_folder_name, unit_id_container.three_star_icon_id),
                'six_star_icon': six_star_icon if six_star_icon is not None else self.image_handler.store_new_icon_images(unit_icon_folder_name, unit_id_container.six_star_icon_id)
            }
            
            character = {
                'unit_id': unit_id,
                'unit_name': name,
                'unit_name_en': romanized_name,
                'jp_thematic': jp_thematic,
                'en_thematic': en_thematic,
                'jp_description': jp_description,
                'en_description': en_description,
                'range': character['search_area_width'],
                'character_icon_locations': character_icon_locations
            } 
            
            self.character_data.append(character)

        character_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, 'character.json')
        with open(character_json_path, 'wb') as character_json_file:
            character_json_file.write(json.dumps(self.character_data, ensure_ascii=False, indent=4).encode("utf8"))
        
    def check_unit_thematic(self, unit_name: str):
        if '(' in unit_name and ')' in unit_name:
            start, end = unit_name.index('('), unit_name.index(')')
            return unit_name[start+1:end]
        return ''
    
    def handle_unit_name(self, unit_name: str):
        actual_unit_name = ''
        if '&' in unit_name:
            name_portions = unit_name.split('&')
            for name_portion in name_portions:
                actual_unit_name = f'{actual_unit_name}&{self.convert_name(name_portion)}' if actual_unit_name != '' else self.convert_name(name_portion)
            return actual_unit_name
        return self.convert_name(unit_name)
    
    def convert_name(self, name):
        japanese_conversion_results = self.kakasi.convert(name)
        for japanese_conversion_result in japanese_conversion_results:
            acutal_unit_name = japanese_conversion_result['hepburn']
        return acutal_unit_name
        
    