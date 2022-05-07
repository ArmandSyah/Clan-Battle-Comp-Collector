import imp
import boto3
from dependency_injector import containers, providers
import pykakasi

from src import manifest_updater, master_db_updater, playable_units_pipeline, bosses_pipeline
from src.utils import master_db_reader, translation_service, image_extraction_service
from src.utils.imagehandler import image_handler 
from src.utils.imagehandler.imagestore import aws_image_store 

class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    s3_resource = providers.Singleton(
        boto3.resource,
        's3',
        aws_access_key_id=config.aws.aws_access_key_id,
        aws_secret_access_key=config.aws.aws_secret_access_key
    )

    kakasi = providers.Singleton(pykakasi.kakasi)

    # Utils

    aws_image_store = providers.Singleton(
        aws_image_store.AwsImageStore
    )

    master_db_reader = providers.Singleton(
        master_db_reader.MasterDBReader,
        config.pcrddatabase.master_db_directory)

    translation_service = providers.Singleton(
        translation_service.TranslationService
    )

    image_extraction_service = providers.Singleton(
        image_extraction_service.ImageExtractionService
    )

    image_handler = providers.Singleton(
        image_handler.ImageHandler
    )

    # Pipeline services

    master_db_updater = providers.Singleton(
        master_db_updater.MasterDBUpdater
    )

    manifest_updater = providers.Singleton(
        manifest_updater.ManifestUpdater
    )

    playable_units_pipeline = providers.Singleton(
        playable_units_pipeline.PlayableUnitsPipeline
    )

    bosses_pipeline = providers.Singleton(
        bosses_pipeline.BossesPipeline
    )