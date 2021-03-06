import logging

import botocore

from src.utils.imagehandler.imagestore.base_image_store import BaseImageStore

class AwsImageStore(BaseImageStore):
    def __init__(self, s3_resource, s3_bucket, s3_region_name) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        self.s3_resource = s3_resource
        self.s3_bucket = s3_bucket
        self.s3_region = s3_region_name
    
    def retrieve(self, image_name) -> str:
        try:
            self.s3_resource.Object(self.s3_bucket, image_name).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                # The object does not exist.
                self.logger.warn(f'Image: {image_name} does not exist in aws bucket {self.s3_bucket}')
                return None
            else:
                # Something else has gone wrong.
                raise
        s3_url = f'https://s3.{self.s3_region}.amazonaws.com/{self.s3_bucket}/{image_name}'
        self.logger.info(f'Getting image from: {s3_url}')
        return s3_url
    
    def store(self, path_of_image_to_store, image_name) -> str:
        self.logger.info(f'Putting image {image_name} into bucket {self.s3_bucket}')
        self.s3_resource.meta.client.upload_file(
            path_of_image_to_store, 
            self.s3_bucket, 
            image_name,
            ExtraArgs={'ACL':'public-read'})