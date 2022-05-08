from collections import defaultdict
import json
import logging
import os

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
        self.clan_battle_schedule_json = config["pipeline_results"]["clan_battle_schedule"]

        self.clan_battle_data = defaultdict(dict)
        self.clan_battle_schedule = defaultdict(dict)
        
    def retrieve_current_bosses(self):
        boss_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, self.boss_json)

        if not os.path.exists(boss_json_path):
            self.logger.debug(f"{self.boss_json} doesn't exist, retrieving fresh boss data")
            self.clan_battle_data = defaultdict(dict)
            return

        with open(boss_json_path, 'r') as boss_json_file:
            try:
                self.clan_battle_data = json.load(boss_json_file)
            except (json.JSONDecodeError):
                self.logger.debug(f'Something went wrong with loading {self.boss_json}, retrieving fresh character data')
                self.clan_battle_data = defaultdict(dict)

    def retrieve_current_schedule(self):
        cb_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, self.clan_battle_schedule_json)

        if not os.path.exists(cb_json_path):
            self.logger.debug(f"{self.clan_battle_schedule_json} doesn't exist, retrieving fresh boss data")
            self.clan_battle_schedule = defaultdict(dict)
            return

        with open(cb_json_path, 'r') as cb_json_file:
            try:
                self.clan_battle_schedule = json.load(cb_json_file)
            except (json.JSONDecodeError):
                self.logger.debug(f'Something went wrong with loading {self.clan_battle_schedule_json}, retrieving fresh character data')
                self.clan_battle_schedule = defaultdict(dict)

    def get_clan_battle_id(self):
        clan_battle_id_query = '''
                                select clan_battle_id 
                                from clan_battle_period 
                                order by start_time desc LIMIT 1
                                '''
        clan_battle_id_result = self.master_db_reader.query_master_db(clan_battle_id_query)
        clan_battle_id = clan_battle_id_result.iloc[0]['clan_battle_id']
        return clan_battle_id

    def build_clan_battle_json(self):
        self.retrieve_current_bosses()
        self.retrieve_current_schedule()

        clan_battle_id = self.get_clan_battle_id()

        if clan_battle_id in self.clan_battle_data:
            self.logger.info("Already pulled latest CB boss data")
            return
        
        self.build_bosses(clan_battle_id)

        if clan_battle_id in self.clan_battle_schedule:
            self.logger.info("Already pulled latest scheudle")
            return
    
        self.build_clan_battle_schedule(clan_battle_id)
        

    def build_bosses(self, clan_battle_id):
        self.logger.info(f'Retrieving boss info for clan battle {clan_battle_id}')

        bosses = []

        clan_battle_info_query = f'''
                                select DISTINCT wave_group_id_1, wave_group_id_2, wave_group_id_3, wave_group_id_4, wave_group_id_5 
                                from clan_battle_2_map_data 
                                where clan_battle_id={clan_battle_id} and phase=1
                                '''
        clan_battle_info_results = self.master_db_reader.query_master_db(clan_battle_info_query)
                                
        clan_battle_info = clan_battle_info_results.iloc[0]

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
            
        for _, boss_info in boss_data_results.iterrows():
            unit_id = boss_info['unit_id']
            
            self.logger.info(f"Processing boss {unit_id}: {boss_info['unit_name']}")
            
            # Name Handling
            jp_name = boss_info['unit_name']
            en_name = self.translator.translate(jp_name)

            # Icons
            boss_icon_dir = self.image_extraction_service.make_unit_icon(en_name, unit_id)
            boss_icon = self.image_handler.check_image_exists(boss_icon_dir, unit_id)
            boss_icon = boss_icon if boss_icon else self.image_handler.store_new_icon_images(boss_icon_dir, unit_id)
            
            boss = {
                'jp_name': jp_name,
                'en_name': en_name,
                'unit_id': unit_id,
                'boss_icon': boss_icon,
                'clan_battle_id': clan_battle_id
            }
            
            bosses.append(boss)
        
        self.clan_battle_data[clan_battle_id] = bosses
                
        boss_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, self.boss_json)
        with open(boss_json_path, 'wb') as boss_json_file:
            boss_json_file.write(json.dumps(self.clan_battle_data, ensure_ascii=False, indent=4).encode("utf8"))

    def build_clan_battle_schedule(self, clan_battle_id):
        clan_battle_period_query = f'''
                                    select clan_battle_id, start_time, end_time  
                                    from clan_battle_period
                                    where clan_battle_id={clan_battle_id}
                                    '''
        
        clan_battle_training_period_query = f'''
                                            select battle_start_time, battle_end_time  
                                            from clan_battle_training_schedule
                                            where clan_battle_id={clan_battle_id}
                                            '''

        clan_battle_period_result = self.master_db_reader.query_master_db(clan_battle_period_query)
        clan_battle_training_period_result = self.master_db_reader.query_master_db(clan_battle_training_period_query)

        clan_battle_period = clan_battle_period_result.iloc[0]
        clan_battle_training_period = clan_battle_training_period_result.iloc[0]

        clan_battle_schedule = {
            'clan_battle_id': clan_battle_id,
            'training_battle_start': clan_battle_training_period['battle_start_time'],
            'training_battle_end': clan_battle_training_period['battle_end_time'],
            'main_battle_start': clan_battle_period['start_time'],
            'main_battle_end': clan_battle_period['end_time'],
        }

        self.clan_battle_schedule[clan_battle_id] = clan_battle_schedule

        cb_json_path = os.path.join(os.getcwd(), self.pipeline_results_directory, self.clan_battle_schedule_json)
        with open(cb_json_path, 'wb') as cb_json_file:
            cb_json_file.write(json.dumps(self.clan_battle_schedule, ensure_ascii=False, indent=4).encode("utf8"))
     