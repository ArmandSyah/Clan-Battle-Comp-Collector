from src.containers import Container

def setup():
    container = Container()
    container.config.from_ini("./config.ini")
    
    # Retrieve a new version of the priconne master database if it exists
    master_db_updater = container.master_db_updater_service()
    master_db_updater.check_and_update_master_db()
    
    manifest_updater = container.manifest_updater_service()
    manifest_updater.get_unit_manifest()
    
    playable_units_pipeline = container.playable_units_pipeline_service()
    playable_units_pipeline.build_character_json()
    
    bosses_pipeline = container.bosses_pipeline_service()
    bosses_pipeline.build_bosses_json()
    
    container.master_db_reader_util().close_connection()
        
if __name__ == "__main__":   
    setup()