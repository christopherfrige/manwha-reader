import boto3
from src.infrastructure.config import SETTINGS


class AWS:
    def __init__(self):
        self.access_key = SETTINGS.aws_access_key
        self.secret_key = SETTINGS.aws_secret_key
        self.region = SETTINGS.aws_region

    def create_session(self) -> boto3.Session:
        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        )
        return session
