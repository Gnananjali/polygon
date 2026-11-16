from django.conf import settings

from .base import (
    StorageBackend,
    problem_prefix,
    test_input_key,
    test_output_key,
)

S3_COMPATIBLE = {"s3", "r2", "minio", "rustfs"}


def get_storage() -> StorageBackend:
    provider = (settings.STORAGE_PROVIDER or "").lower()
    if provider in S3_COMPATIBLE:
        from .s3_backend import S3Backend
        return S3Backend(
            bucket=settings.S3_BUCKET_NAME,
            endpoint_url=settings.S3_ENDPOINT_URL,
            access_key=settings.S3_ACCESS_KEY_ID,
            secret_key=settings.S3_SECRET_ACCESS_KEY,
            region=settings.S3_REGION,
        )
    raise ValueError(f"Unsupported STORAGE_PROVIDER: {provider!r}")