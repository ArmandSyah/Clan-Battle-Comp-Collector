import os

from src.containers import Container

def setup():
    container = Container()
    container.config.aws_access_key_id.from_env("AWS_ACCESS_KEY_ID")
    container.config.aws_secret_access_key.from_env("AWS_SECRET_ACCESS_KEY")
    container.config.deepl_api_key.from_env("DEEPL_API_KEY")
    container.config.yandex_api_key.from_env("YANDEX_API_KEY")
    container.config.microsoft_api_key.from_env("MICROSOFT_API_KEY")
    container.init_resources()
    
    # Retrieve a new version of the priconne master database if it exists
    master_db_updater = container.master_db_updater_service()
    master_db_updater.check_and_update_master_db()
    
    manifest_updater = container.manifest_updater_service()
    manifest_updater.get_unit_manifest()
    
    playable_units_pipeline = container.playable_units_pipeline_service()
    playable_units_pipeline.build_character_json()
    
    bosses_pipeline = container.bosses_pipeline_service()
    bosses_pipeline.build_clan_battle_json()
    
    container.master_db_reader_util().close_connection()
        
if __name__ == "__main__":   
    if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
        os.mkdir(os.path.join(os.getcwd(), 'logs'))
    
    setup()