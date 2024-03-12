from src.infrastructure.services.aws import AWS
from src.infrastructure.config import SETTINGS


class S3Service(AWS):
    def __init__(self):
        super().__init__()
        self.bucket_name = SETTINGS.aws_bucket_name
        self.s3 = self.create_session().resource("s3")

    def upload_object(self, local_file_path: str, s3_key: str):
        try:
            self.s3.Bucket(self.bucket_name).upload_file(local_file_path, s3_key)
            print(f"Object uploaded successfully to S3: s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error uploading object to S3: {e}")

    def download_object(self, local_file_path: str, s3_key: str):
        try:
            self.s3.Bucket(self.bucket_name).download_file(s3_key, local_file_path)
            print(f"Object downloaded successfully from S3: s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error downloading object from S3: {e}")

    def list_objects(self, prefix: str = ""):
        try:
            objects = self.s3.Bucket(self.bucket_name).objects.filter(Prefix=prefix)
            for obj in objects:
                print(f"Object in S3: s3://{self.bucket_name}/{obj.key}")
        except Exception as e:
            print(f"Error listing objects in S3: {e}")


if __name__ == "__main__":
    s3 = S3Service()

    # s3.upload_object('teste.txt', 'teste/teste.txt')
    s3.list_objects()
