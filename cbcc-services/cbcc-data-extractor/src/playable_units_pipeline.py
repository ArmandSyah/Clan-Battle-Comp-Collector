from collections import defaultdict
import json
import logging
import os

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
        self.character_data = defaultdict(dict)
        
    
    def retrieve_current_character_info(self):
        character_json_path = os.path.join(os.getcwd(),self.pipeline_results_directory, self.character_json)
        
        if not os.path.exists(character_json_path):
            self.logger.debug('Character.json doesn\'t exist, retrieving fresh character data')
            self.current_thematics = dict()
            self.retrieved_unit_ids = set()
            self.character_data = defaultdict(dict)
            return
        
        with open(character_json_path, 'rb') as character_json_file:
            try:
                self.character_data = json.load(character_json_file)
                self.retrieved_unit_ids = set(unit_id for unit_id in self.character_data.keys())
                thematics_from_data = set((character['jp_thematic'], character['en_thematic']) for character in self.character_data.values()) 
                self.current_thematics = {jp_thematic:en_thematic for (jp_thematic, en_thematic) in thematics_from_data}    
            except (json.JSONDecodeError):
                self.logger.debug(f'Something went wrong with loading {self.character_json}, retrieving fresh character data')
                self.current_thematics = dict()
                self.retrieved_unit_ids = set()
                self.character_data = defaultdict(dict)
            
        
    def build_character_json(self):
        self.retrieve_current_character_info()
        
        character_query = '''
                        select unit_id, unit_name, prefab_id, search_area_width, comment
                        from unit_data
                        where unit_id < 190000 and comment <> ''
                        order by search_area_width 
                        '''
        
        character_results = self.master_db_reader.query_master_db(character_query)
        
        for _, character_result in character_results.iterrows():
            unit_id = character_result['unit_id']
            
            if unit_id in self.retrieved_unit_ids:
                self.update_character(character_result)
            else:
                self.add_character(character_result)

        character_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, 'character.json')
        with open(character_json_path, 'wb') as character_json_file:
            character_json_file.write(json.dumps(self.character_data, ensure_ascii=False, indent=4).encode("utf8"))

    def update_character(self, character_result):
        unit_id = character_result['unit_id']
        current_character_data = self.character_data[unit_id]

        self.logger.info(f"Checking if character {unit_id} needs update")

        is_six_star = current_character_data['max_star'] == 6 or self.check_unit_six_star(unit_id)

        if is_six_star and current_character_data['max_star'] != 6:
            # Only update case concerned is if an existing character has gotten a 6* update
            self.logger.debug(f"Update required for {unit_id}")

            icon_id = self.get_icon_id(unit_id, is_six_star)
            icon_path = self.image_extraction_service.make_unit_icon(current_character_data['unit_name_en'], icon_id, current_character_data['en_thematic'])
            ### Checking for existance of icons in the image store first
            icon = self.image_handler.check_image_exists(icon_path, icon_id)

            self.character_data[unit_id]['icon'] = icon
            self.character_data[unit_id]['max_star'] = 6
            self.character_data[unit_id]['update_action'] = 'update'
        else:
            self.logger.debug(f"No update required for {unit_id}")
            self.character_data[unit_id]['update_action'] = 'no_op'


    def add_character(self, character_result):
        unit_id = character_result['unit_id']

        self.logger.info(f"Processing new character {unit_id}: {character_result['unit_name']}")
        
        range = character_result['search_area_width']
        if range == '0':
            return

        # thematics
        jp_thematic = self.check_unit_thematic(character_result["unit_name"])
        if not jp_thematic in self.current_thematics:
            en_thematic = self.translator.translate(jp_thematic)
            self.current_thematics[jp_thematic] = en_thematic.capitalize()
        else:
            en_thematic = self.current_thematics[jp_thematic]

        name = character_result["unit_name"].split('(')[0]
        # Get the romanized string of the katakana
        romanized_name = self.handle_unit_name(name)

        # Check if unit is a 6*
        is_six_star = self.check_unit_six_star(unit_id)
        icon_id = self.get_icon_id(unit_id, is_six_star)
        icon_path = self.image_extraction_service.make_unit_icon(romanized_name, icon_id, en_thematic)

        ### Checking for existance of icons in the image store first
        icon = self.image_handler.check_image_exists(icon_path, icon_id)
        icon = icon if icon else self.image_handler.store_new_icon_images(icon_path, icon_id)

        character = {
            'unit_id': unit_id,
            'unit_name': name,
            'unit_name_en': romanized_name,
            'jp_thematic': jp_thematic,
            'en_thematic': en_thematic,
            'range': range,
            'character_icon': icon,
            'update_action': 'new', # other values include '' or 'update'
            'max_star': 6 if is_six_star else 5
        }

        self.character_data[unit_id] = character


    def check_unit_six_star(self, unit_id):
        six_star_query = f'''
                        select count(unit_id) 
                        from unit_rarity
                        where unit_id={unit_id} and rarity=6 
                        '''
        query_results = self.master_db_reader.query_master_db(six_star_query)

        return int(query_results.iloc[0]['count(unit_id)']) > 0

    def get_icon_id(self, unit_id, is_six_star):
        return f'{unit_id[0:4]}6{unit_id[5]}' if is_six_star else f'{unit_id[0:4]}3{unit_id[5]}'

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
            acutal_unit_name = japanese_conversion_result['hepburn'].capitalize()
        return acutal_unit_name
        
    