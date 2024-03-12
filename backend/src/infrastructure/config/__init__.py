from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_environment: str = "development"

    db_host: str = "localhost"
    db_user: str = "postgres"
    db_password: str = "password"
    db_port: str = "5432"
    db_name: str = "manwha_reader"
    db_driver: str = "postgresql+psycopg2"

    aws_access_key: str = "AKIA2CKEVD2VPYDFKXNE"
    aws_secret_key: str = "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"
    aws_region: str = "sa-east-1"
    aws_bucket_name: str = "manwha-reader"
    aws_bucket_url: str = f"http://{aws_bucket_name}.s3.amazonaws.com"


SETTINGS = _Settings()
