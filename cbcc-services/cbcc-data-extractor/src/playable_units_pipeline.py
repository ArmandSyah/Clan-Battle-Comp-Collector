import json
import os

from pykakasi.kakasi import Kakasi
from src.utils.master_db_reader import MasterDBReader
from src.utils.config_reader import ConfigReader
from src.utils.translation_service import TranslationService

class PlayableUnitsPipeline:
    def __init__(self, config_reader: ConfigReader, master_db_reader: MasterDBReader, kakasi: Kakasi, translator: TranslationService) -> None:
        self.config_reader = config_reader
        self.master_db_reader = master_db_reader
        self.kakasi = kakasi
        self.translator = translator
        
        self.current_thematics = dict()
        
        ## Configs
        self.pipeline_results_directory = config_reader.read('pipeline_results_directory')
        
    def build_character_json(self):
        character_query = '''
                        select unit_id, unit_name, prefab_id, search_area_width, comment
                        from unit_data
                        where unit_id < 190000 and comment <> ''
                        order by search_area_width 
                        '''
        
        character_results = self.master_db_reader.query_master_db(character_query)
        
        character_data = []
        
        for _, row in character_results.iterrows():
            print(f"Processing character {row['unit_id']}: {row['unit_name']}")
            # thematics
            jp_thematic = self.check_unit_thematic(row["unit_name"])
            
            if not jp_thematic in self.current_thematics:
                en_thematic = self.translator.translate(jp_thematic)
                self.current_thematics[jp_thematic] = en_thematic
            else:
                en_thematic = self.current_thematics[jp_thematic]
            
            name = row["unit_name"].split('(')[0]
            # Get the romanized string of the katakana
            japanese_conversion_results = self.kakasi.convert(name)
            for japanese_conversion_result in japanese_conversion_results:
                romanized_name = japanese_conversion_result['hepburn']
            
            jp_description = row["comment"].replace(r'\n', '')
            en_description = self.translator.translate(jp_description)
            
            character = {
                'unit_id': row["unit_id"],
                'unit_name': name,
                'unit_name_en': romanized_name,
                'jp_thematic': jp_thematic,
                'en_thematic': en_thematic,
                'jp_description': jp_description,
                'en_description': en_description
            } 
            
            character_data.append(character)

        character_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, 'character.json')
        with open(character_json_path, 'wb') as character_json_file:
            character_json_file.write(json.dumps(character_data, ensure_ascii=False, indent=4).encode("utf8"))
        
    def check_unit_thematic(self, unit_name: str):
        if '(' in unit_name and ')' in unit_name:
            start, end = unit_name.index('('), unit_name.index(')')
            return unit_name[start+1:end]
        return ''
    