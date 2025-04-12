"""S3 presigned URL 생성."""

import boto3
from botocore.exceptions import ClientError
from typing import Optional

from housing_alert.config import settings

s3 = boto3.client("s3", region_name=settings.aws_region)


def create_presigned_url(object_key: str, expires: int = 3600) -> Optional[str]:
    try:
        return s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.S3_BUCKET, "Key": object_key},
            ExpiresIn=expires,
        )
    except ClientError as e:
        print("S3 presigned URL error", e)
        return None
