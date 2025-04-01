import os
import boto3
from django.apps import AppConfig
from django.conf import settings
from botocore.exceptions import ClientError


class LearnblocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learnblocks'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return  # Skip the duplicate call in dev server
        options = settings.STORAGES['default']["OPTIONS"]
        bucket_name = "learnblocks"

        s3 = boto3.client("s3", aws_access_key_id=options['access_key'],
                          aws_secret_access_key=options['secret_key'],
                          endpoint_url=options['endpoint_url'],
                          region_name=options['region_name'])
        try:
            s3.head_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' already exists.")
        except ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                print(f"Bucket '{bucket_name}' not found. Creating it...")
                s3.create_bucket(Bucket=bucket_name,
                                 CreateBucketConfiguration={
                                     "LocationConstraint":
                                         options.get("region_name",
                                                     "us-east-2")},)
            else:
                raise e
