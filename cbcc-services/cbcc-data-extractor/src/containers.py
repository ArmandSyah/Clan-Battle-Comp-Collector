import imp
import logging.config
import boto3
from dependency_injector import containers, providers
import pykakasi

from src import manifest_updater, master_db_updater, playable_units_pipeline, bosses_pipeline
from src.utils import master_db_reader, translation_service, image_extraction_service
from src.utils.imagehandler import image_handler 
from src.utils.imagehandler.imagestore import aws_image_store 

class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini"
    )

    s3_resource = providers.Singleton(
        boto3.resource,
        's3',
        aws_access_key_id=config.aws.aws_access_key_id,
        aws_secret_access_key=config.aws.aws_secret_access_key
    )

    kakasi = providers.Singleton(pykakasi.kakasi)

    # Utils

    aws_image_store_util = providers.Singleton(
        aws_image_store.AwsImageStore,
        s3_resource,
        config.aws.s3_bucket,
        config.aws.s3_region_name
    )

    master_db_reader_util = providers.Singleton(
        master_db_reader.MasterDBReader,
        config.directories.master_db_directory,
        config.pcrddatabase.master_db)

    translation_service_util = providers.Singleton(
        translation_service.TranslationService,
        config
    )

    image_extraction_service_util = providers.Singleton(
        image_extraction_service.ImageExtractionService,
        config
    )

    image_handler_util = providers.Singleton(
        image_handler.ImageHandler,
        aws_image_store_util,
        config.directories.temp_assets_directory,
        config.directories.deserialized_assets_directory
    )

    # Pipeline services

    master_db_updater_service = providers.Singleton(
        master_db_updater.MasterDBUpdater,
        config
    )

    manifest_updater_service = providers.Singleton(
        manifest_updater.ManifestUpdater,
        config
    )

    playable_units_pipeline_service = providers.Singleton(
        playable_units_pipeline.PlayableUnitsPipeline,
        master_db_reader_util,
        kakasi,
        translation_service_util,
        image_extraction_service_util,
        image_handler_util,
        config
    )

    bosses_pipeline_service = providers.Singleton(
        bosses_pipeline.BossesPipeline,
        master_db_reader_util,
        translation_service_util,
        image_extraction_service_util,
        image_handler_util,
        config
    )