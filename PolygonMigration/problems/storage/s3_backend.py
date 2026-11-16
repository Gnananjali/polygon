import boto3
from botocore.client import Config

from .base import StorageBackend


class S3Backend(StorageBackend):
    def __init__(self, bucket, endpoint_url=None, access_key=None,
                 secret_key=None, region=None):
        self.bucket = bucket
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url or None,
            aws_access_key_id=access_key or None,
            aws_secret_access_key=secret_key or None,
            region_name=region or "us-east-1",
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
                request_checksum_calculation="when_required",
                response_checksum_validation="when_required",
            ),
        )

    def upload(self, key, data):
        self.client.put_object(Bucket=self.bucket, Key=key, Body=data)

    def delete_prefix(self, prefix):
        deleted = 0
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            objects = [{"Key": o["Key"]} for o in page.get("Contents", [])]
            if objects:
                self.client.delete_objects(
                    Bucket=self.bucket, Delete={"Objects": objects}
                )
                deleted += len(objects)
        return deleted