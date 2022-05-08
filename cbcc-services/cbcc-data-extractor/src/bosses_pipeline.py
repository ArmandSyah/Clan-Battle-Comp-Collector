import json
import logging
import os

from src.models.unit_id_container import UnitIdContainer

class BossesPipeline:
    def __init__(self, master_db_reader, translator, image_extraction_service, image_handler, config) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        self.master_db_reader = master_db_reader
        self.translator = translator
        self.image_extraction_service = image_extraction_service
        self.image_handler = image_handler
        
        ## Configs
        self.pipeline_results_directory = config["directories"]["pipeline_results_directory"]
        self.boss_json = config["pipeline_results"]["boss"]
        
        self.cached_en_names = dict()
        self.cached_en_desription_translations = dict()
        self.cached_boss_icons = dict()
        
    
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
                unit_id = boss_info['unit_id']
                
                self.logger.info(f"Processing boss {unit_id}: {boss_info['unit_name']}")
                # Name Handling
                jp_name = boss_info['unit_name']
                if jp_name in self.cached_en_names:
                    en_name = self.cached_en_names[jp_name]
                else:
                    en_name = self.translator.translate(jp_name)
                    self.cached_en_names[jp_name] = en_name
                
                # Descriptions
                jp_description = boss_info["comment"].replace('\n', '')
                if jp_name in self.cached_en_desription_translations:
                    en_description = self.cached_en_desription_translations[jp_name]
                else:
                    en_description = self.translator.translate(jp_description)
                    self.cached_en_desription_translations[jp_name] = en_description
                
                # Icons
                if jp_name in self.cached_boss_icons:
                    boss_icon = self.cached_boss_icons[jp_name]
                else:
                    unit_id_container = UnitIdContainer(unit_id, False)
                    unit_icon_folder_name = self.image_extraction_service.make_unit_icons(en_name, unit_id_container)
                    boss_icon = self.image_handler.check_image_exists(unit_icon_folder_name, unit_id_container.unit_id)
                    boss_icon = boss_icon if boss_icon is not None else self.image_handler.store_new_icon_images(unit_icon_folder_name, unit_id_container.unit_id)
                    self.cached_boss_icons[jp_name] = boss_icon
                
                boss = {
                    'jp_name': jp_name,
                    'en_name': en_name,
                    'unit_id': unit_id,
                    'level': boss_info['level'],
                    'hp': boss_info['hp'],
                    'jp_description': jp_description,
                    'en_description': en_description,
                    'boss_icon': boss_icon
                }
                
                full_tier['boss_data'].append(boss)
            
            full_clan_battle_data.append(full_tier)
                
        boss_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, self.boss_json)
        with open(boss_json_path, 'wb') as boss_json_file:
            boss_json_file.write(json.dumps(full_clan_battle_data, ensure_ascii=False, indent=4).encode("utf8")) 