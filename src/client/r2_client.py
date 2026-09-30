import boto3

from config.settings import (
    R2_ACCOUNT_ID,
    R2_ACCESS_KEY_ID,
    R2_SECRET_ACCESS_KEY,
)


class R2Client:
    """
    Client for Cloudflare R2 using the S3-compatible API.
    """

    def __init__(self):

        endpoint_url = (
            f"https://{R2_ACCOUNT_ID}"
            ".r2.cloudflarestorage.com"
        )

        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )

    def upload_file(
        self,
        file_path,
        bucket,
        object_key,
    ):
        """
        Upload a local file to R2.
        """

        self.client.upload_file(
            file_path,
            bucket,
            object_key,
        )

        print(
            f"Uploaded: s3://{bucket}/{object_key}"
        )