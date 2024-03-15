from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_environment: str = "development"

    db_host: str = "postgres"
    db_user: str = "postgres"
    db_password: str = "password"
    db_port: str = "5432"
    db_name: str = "manwha_reader"
    db_driver: str = "postgresql+psycopg2"

    aws_access_key: str = "your_aws_access_key"
    aws_secret_key: str = "your_aws_secret_key"
    aws_region: str = "your_aws_region"
    aws_bucket_name: str = "your_bucket_name"
    aws_bucket_url: str = f"http://{aws_bucket_name}.s3.amazonaws.com"

    frontend_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env")


SETTINGS = _Settings()
