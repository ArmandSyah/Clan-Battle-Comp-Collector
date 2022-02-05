import boto3
import botocore

from src.utils.env_reader import EnvReader
from src.utils.imagehandler.imagestore.base_image_store import BaseImageStore

class AwsImageStore(BaseImageStore):
    def __init__(self, env_reader: EnvReader) -> None:
        self.env_reader = env_reader
        
        # env variables
        self.s3_key = self.env_reader.read('AWS_ACCESS_KEY_ID')
        self.s3_secret = self.env_reader.read('AWS_SECRET_ACCESS_KEY')
        self.s3_bucket = self.env_reader.read('S3_BUCKET')
        self.s3_region = self.env_reader.read('S3_REGION_NAME')
        
        self.s3_resource = boto3.resource('s3', 
                                          aws_access_key_id=self.s3_key, 
                                          aws_secret_access_key=self.s3_secret)
    
    def retrieve(self, image_name) -> str:
        try:
            self.s3_resource.Object(self.s3_bucket, image_name).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                # The object does not exist.
                print(f'Image: {image_name} does not exist in aws bucket {self.s3_bucket}')
                return None
            else:
                # Something else has gone wrong.
                raise
        return f'https://s3.{self.s3_region}.amazonaws.com/{self.s3_bucket}/{image_name}'
    
    def store(self, path_of_image_to_store, image_name) -> str:
        self.s3_resource.meta.client.upload_file(
            path_of_image_to_store, 
            self.s3_bucket, 
            image_name,
            ExtraArgs={'ACL':'public-read'})