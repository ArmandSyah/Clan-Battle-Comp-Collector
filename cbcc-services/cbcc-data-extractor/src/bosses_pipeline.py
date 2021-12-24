import json
import os

from src.utils.master_db_reader import MasterDBReader
from src.utils.config_reader import ConfigReader
from src.utils.translation_service import TranslationService

class BossesPipeline:
    def __init__(self, config_reader: ConfigReader, master_db_reader: MasterDBReader, translator: TranslationService) -> None:
        self.config_reader = config_reader
        self.master_db_reader = master_db_reader
        self.translator = translator
        
        ## Configs
        self.pipeline_results_directory = config_reader.read('pipeline_results_directory')
        
        self.cached_translations = dict()
        
    
    def build_bosses_json(self):
        clan_battle_info_query = '''
                                select DISTINCT phase, wave_group_id_1, wave_group_id_2, wave_group_id_3, wave_group_id_4, wave_group_id_5 
                                from clan_battle_2_map_data 
                                where clan_battle_id=(select clan_battle_id 
                                                    from clan_battle_period 
                                                    order by start_time desc LIMIT 1);
                                '''
                                
        clan_battle_info_results = self.master_db_reader.query_master_db(clan_battle_info_query)
                                
        full_clan_battle_data = []
        
        for _, clan_battle_info in clan_battle_info_results.iterrows():
            phase = clan_battle_info['phase']
            boss_1_key = clan_battle_info['wave_group_id_1'] 
            boss_2_key = clan_battle_info['wave_group_id_2']  
            boss_3_key = clan_battle_info['wave_group_id_3'] 
            boss_4_key = clan_battle_info['wave_group_id_4'] 
            boss_5_key = clan_battle_info['wave_group_id_5']
            
            boss_data_query = f'''
                                select u.unit_id, u.unit_name, e.level, e.hp, u.comment
                                from wave_group_data w
                                inner join enemy_parameter e on w.enemy_id_1 = e.enemy_id
                                inner join unit_enemy_data u on e.unit_id = u.unit_id
                                where wave_group_id in ({boss_1_key}, {boss_2_key}, {boss_3_key}, {boss_4_key}, {boss_5_key})
                                order by e.level asc; 
                            '''
            
            boss_data_results = self.master_db_reader.query_master_db(boss_data_query)
            
            full_tier = {
                'tier': phase,
                'boss_data': []
            }
            
            for _, boss_info in boss_data_results.iterrows():
                
                # Checking for cached translations if they exist
                cached_translation = None
                if boss_info["unit_id"] in self.cached_translations:
                    cached_translation = self.cached_translations[boss_info["unit_id"]]
                
                # Name Handling
                jp_name = boss_info['unit_name'] if cached_translation is None else cached_translation['jp_name']
                en_name = self.translator.translate(jp_name) if cached_translation is None else cached_translation['en_name']
                
                # Descriptions
                jp_description = boss_info["comment"].replace(r'\n', '') if cached_translation is None else cached_translation['jp_description']
                en_description = self.translator.translate(jp_description) if cached_translation is None else cached_translation['en_description']
                
                # Setup cached translation object for future use to reduce repeated work
                if cached_translation is None:
                    cached_translation = {
                        'jp_name': jp_name,
                        'en_name': en_name,
                        'jp_description': jp_description,
                        'en_description': en_description
                    }
                    self.cached_translations[boss_info["unit_id"]] = cached_translation
                
                boss = {
                    'jp_name': jp_name,
                    'en_name': en_name,
                    'unit_id': boss_info['unit_id'],
                    'level': boss_info['level'],
                    'hp': boss_info['hp'],
                    'jp_description': jp_description,
                    'en_description': en_description
                }
                
                full_tier['boss_data'].append(boss)
            
            full_clan_battle_data.append(full_tier)
            
        boss_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, 'boss.json')
        with open(boss_json_path, 'wb') as boss_json_file:
            boss_json_file.write(json.dumps(full_clan_battle_data, ensure_ascii=False, indent=4).encode("utf8")) 