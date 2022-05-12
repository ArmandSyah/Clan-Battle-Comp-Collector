from datetime import datetime
import errno
import json
import logging
import os

import requests


class PipelineExporter:
    def __init__(self, config):
        self.logger = logging.getLogger('dataExtractorLogger')

        self.tsumugi_endpoint = config["endpoints"]["tsumugi"]

        self.pipeline_results_directory = config["directories"]["pipeline_results_directory"]
        self.character_json = config["pipeline_results"]["character"]
        self.boss_json = config["pipeline_results"]["boss"]
        self.clan_battle_schedule_json = config["pipeline_results"]["clan_battle_schedule"]

    def export(self):
        self.logger.info('Exporting pipeline data')
        current_dir = os.getcwd()

        ## checking that the json is present
        character_dir = os.path.join(current_dir, self.pipeline_results_directory, self.character_json)
        boss_dir = os.path.join(current_dir, self.pipeline_results_directory, self.boss_json)
        clan_battle_schedule_dir = os.path.join(current_dir, self.pipeline_results_directory, self.clan_battle_schedule_json)

        if not os.path.exists(character_dir):
            self.logger.error(f'{character_dir} does not exist, terminating pipeline')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.character_json)
        
        if not os.path.exists(boss_dir):
            self.logger.error(f'{boss_dir} does not exist, terminating pipeline')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.boss_json)

        if not os.path.exists(clan_battle_schedule_dir):
            self.logger.error(f'{clan_battle_schedule_dir} does not exist, terminating pipeline')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.clan_battle_schedule_json)

        with open(character_dir, 'rb') as character_json_file:
            try:
                character_data = json.load(character_json_file)
                self.process_character_data(character_data)
            except:
                self.logger.error(f'Something went wrong when loading data from {self.character_json}')
                raise

        with open(clan_battle_schedule_dir, 'rb') as clan_battle_json_file:
            try:
                clan_battle_schedule_data = json.load(clan_battle_json_file)
                self.process_clan_battle_schedule_data(clan_battle_schedule_data)
            except:
                self.logger.error(f'Something went wrong when loading data from {self.clan_battle_schedule_json}')
                raise

        with open(boss_dir, 'rb') as boss_json_file:
            try:
                boss_data = json.load(boss_json_file)
                self.process_boss_data(boss_data)
            except:
                self.logger.error(f'Something went wrong when loading data from {self.boss_json}')
                raise  


    def process_character_data(self, character_data):
        character_endpoint = f'{self.tsumugi_endpoint}/characters'

        for character in character_data.values():
            update_action = character['update_action']

            unit_id = int(character['unit_id'])
            unit_name = character['unit_name']
            unit_name_en = character['unit_name_en']
            jp_thematic = character['jp_thematic']
            en_thematic = character['en_thematic']
            range = int(character['range'])
            character_icon = character['character_icon']
            max_star = int(character['max_star'])

            if update_action == 'new':
                post_data = {
                    'unit_id': unit_id,
                    'unit_name': unit_name,
                    'unit_name_en': unit_name_en,
                    'thematic': jp_thematic,
                    'thematic_en': en_thematic,
                    'range': range,
                    'icon': character_icon,
                    'max_star': max_star
                }
                self._post_request(character_endpoint, post_data)
            elif update_action == 'update':
                update_character_endpoint = f'{character_endpoint}/{int(unit_id)}'
                put_data = { 'max_star': character['max_star']}
                self._put_request(update_character_endpoint, put_data)

    def process_clan_battle_schedule_data(self, clan_battle_schedule):
        clan_battle_endpoint = f'{self.tsumugi_endpoint}/clanbattle'

        for clan_battle in clan_battle_schedule.values():
            clan_battle_id = int(clan_battle['clan_battle_id'])
            training_battle_start = clan_battle['training_battle_start']
            training_battle_end = clan_battle['training_battle_end']
            main_battle_start = clan_battle['main_battle_start']
            main_battle_end = clan_battle['main_battle_end']

            post_data = {
                'clan_battle_id': clan_battle_id,
                'training_start_date': training_battle_start,
                'training_end_date': training_battle_end,
                'main_start_date': main_battle_start,
                'main_end_date': main_battle_end
            }

            self._post_request(clan_battle_endpoint, post_data)

    def process_boss_data(self, boss_data):
        boss_endpoint = f'{self.tsumugi_endpoint}/bosses'

        for boss_list in boss_data.values():
            for boss in boss_list:
                unit_id = int(boss['unit_id'])
                unit_name = boss['jp_name']
                unit_name_en = boss['en_name']
                icon = boss['boss_icon']
                clan_battle_id = int(boss['clan_battle_id'])

                post_data = {
                    'unit_id': unit_id,
                    'unit_name': unit_name,
                    'unit_name_en': unit_name_en,
                    'icon': icon,
                    'clan_battle_id': clan_battle_id,
                }

                self._post_request(boss_endpoint, post_data)

    def _post_request(self, endpoint, post_data):
        try:
            self.logger.debug(f'Sending a post request to {endpoint}')
            headers = {'Content-type': 'application/json'}
            r = requests.post(endpoint, json=post_data, headers=headers, timeout=10.0)
            r.raise_for_status()
            self.logger.debug(f'Sucessfully sent a post request to {endpoint}')
        except requests.HTTPError as e:
            self.logger.warn(f'Error while sending data: \n{e}')
            self.logger.debug(r.text)

    def _put_request(self, endpoint, data):
        try:
            self.logger.debug(f'Sending a post request to {endpoint}')
            headers = {'Content-type': 'application/json'}
            r = requests.put(endpoint, json=data, headers=headers, timeout=10.0)
            r.raise_for_status()
            self.logger.debug(f'Sucessfully sent a post request to {endpoint}')
        except requests.HTTPError as e:
            self.logger.warn(f'Error while sending data: \n{e}')
            self.logger.debug(r.text)
           
            

