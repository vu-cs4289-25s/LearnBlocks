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
