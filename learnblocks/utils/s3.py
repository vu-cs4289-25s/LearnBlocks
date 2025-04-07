import os
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def get_path(instance, filepath):
    name = instance.__class__.__name__
    plural = 'es' if name[-1] == 's' else 's'
    pl_name = name + plural
    id_field = instance.s3_key_id
    id = getattr(instance, id_field)
    return f'{pl_name}/{id}'


def ensure_bucket_exists(bucket_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            print(f"[MinIO] Bucket '{bucket_name}' not found. Creating it...")
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": settings.AWS_S3_REGION_NAME
                }
            )
        else:
            raise e


def connect_s3():
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

