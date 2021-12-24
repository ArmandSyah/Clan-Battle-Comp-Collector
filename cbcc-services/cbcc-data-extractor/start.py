import os

import pykakasi

from src.master_db_updater import MasterDBUpdater
from src.playable_units_pipeline import PlayableUnitsPipeline
from src.utils.config_reader import ConfigReader
from src.utils.env_reader import EnvReader
from src.utils.master_db_reader import MasterDBReader
from src.utils.translation_service import TranslationService
from src.bosses_pipeline import BossesPipeline
        
if __name__ == "__main__":
    config_reader = ConfigReader('config.json')
    env_reader = EnvReader('.env')
    
    # Retrieve a new version of the priconne master database if it exists
    master_db_updater = MasterDBUpdater(config_reader)
    master_db_updater.check_and_update_master_db()
    
    # Setup path to current master db and instantiate master db reader
    current_dir = os.getcwd()
    database_directory = config_reader.read("database", "master_db_directory")
    current_hash = config_reader.read("database", "current_hash")
    
    master_db_path = os.path.join(current_dir, database_directory, f'master_{current_hash}.db')
    master_db_reader = MasterDBReader(master_db_path)
    
    kakasi = pykakasi.kakasi()
    
    translator = TranslationService(config_reader, env_reader)
    
    if not os.path.exists(os.path.join(current_dir, config_reader.read('pipeline_results_directory'))):
        os.makedirs(os.path.join(current_dir, config_reader.read('pipeline_results_directory')))
    
    # playable_units_pipeline = PlayableUnitsPipeline(config_reader, master_db_reader, kakasi, translator)
    # playable_units_pipeline.build_character_json()
    
    bosses_pipeline = BossesPipeline(config_reader, master_db_reader, translator)
    bosses_pipeline.build_bosses_json()
    
    master_db_reader.close_connection()