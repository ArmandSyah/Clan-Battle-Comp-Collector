import logging
import os
import shutil

class PipelineStaging:
    def __init__(self, config):
        self.logger = logging.getLogger('dataExtractorLogger')

        self.manifest_directory = config["directories"]["manifest_directory"]
        self.pipeline_results_directory = config["directories"]["pipeline_results_directory"]
        self.temp_assets_directory = config["directories"]["temp_assets_directory"]
        self.master_db_directory = config["directories"]["master_db_directory"]
        self.api_version_directory = config["directories"]["api_version_directory"]
        
        self.staging_action = config["staging_action"]

    def stage(self):
        if self.staging_action == "init":
            self._run_init()

    def _run_init(self):
        self.logger.info("Fresh retrieval, removing various directories")

        current_dir = os.getcwd()

        manifest_path = os.path.join(current_dir, self.manifest_directory)
        pipeline_results_path = os.path.join(current_dir, self.pipeline_results_directory)
        temp_assets_path = os.path.join(current_dir, self.temp_assets_directory)
        master_db_path = os.path.join(current_dir, self.master_db_directory)
        api_version_path = os.path.join(current_dir, self.api_version_directory)

        shutil.rmtree(manifest_path)
        shutil.rmtree(pipeline_results_path)
        shutil.rmtree(temp_assets_path)
        shutil.rmtree(master_db_path)
        shutil.rmtree(api_version_path)
