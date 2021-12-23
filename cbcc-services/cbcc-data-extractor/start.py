from src.master_db_updater import MasterDBUpdater
from src.utils.config_reader import ConfigReader
        
if __name__ == "__main__":
    config_reader = ConfigReader('config.json')
    master_db_updater = MasterDBUpdater(config_reader)
    master_db_updater.check_and_update_master_db()