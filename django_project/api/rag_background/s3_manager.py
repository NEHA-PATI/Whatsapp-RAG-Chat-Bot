# from io import BytesIO

# THREE_DAYS_IN_SECONDS = 259200


# def upload_file(path: str, content: BytesIO, public_url_expiry_seconds=THREE_DAYS_IN_SECONDS) -> str:
#     """
#     todo: neha
#     return publicly readable s3 url which expires in public_url_expiry_seconds
#     """


import boto3
import os
from io import BytesIO

THREE_DAYS_IN_SECONDS = 259200

# Load environment variables
_bucket = os.getenv("S3_BUCKET_NAME")
_region = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")

# Create S3 client
_s3 = boto3.client(
    "s3",
    region_name=_region,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def upload_file(path: str, content: BytesIO, public_url_expiry_seconds=THREE_DAYS_IN_SECONDS) -> str:
    """
    Uploads a file to S3 and returns a presigned URL that expires in given seconds.
    """
    # Upload file to S3
    _s3.put_object(Bucket=_bucket, Key=path, Body=content)

    # Generate presigned URL
    url = _s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': _bucket, 'Key': path},
        ExpiresIn=public_url_expiry_seconds
    )
    return url
