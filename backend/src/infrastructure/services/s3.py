from src.infrastructure.services.aws import AWS
from src.infrastructure.config import SETTINGS


class S3Service(AWS):
    def __init__(self):
        super().__init__()
        self.bucket_name = SETTINGS.aws_bucket_name
        self.s3 = self.create_session().resource("s3")

    def upload_object(self, local_path: str, storage_path: str):
        try:
            self.s3.Bucket(self.bucket_name).upload_file(local_path, storage_path)
            print(f"Object uploaded to S3: s3://{self.bucket_name}/{storage_path}")
        except Exception as e:
            print(f"Error uploading object to S3: {e}")

    def download_object(self, local_file_path: str, s3_key: str):
        try:
            self.s3.Bucket(self.bucket_name).download_file(s3_key, local_file_path)
            print(f"Object downloaded from S3: s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error downloading object from S3: {e}")

    def list_objects(self, path: str = "") -> list | None:
        try:
            objects = self.s3.Bucket(self.bucket_name).objects.filter(Prefix=path)
            return [obj.key for obj in objects]
        except Exception as e:
            print(f"Error listing objects in S3: {e}")
