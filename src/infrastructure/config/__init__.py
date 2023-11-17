from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    app_environment: str = "development"

    db_host: str = "localhost"
    db_user: str = "postgres"
    db_password: str = "password"
    db_port: str = "5432"
    db_name: str = "manwha_reader"
    db_driver: str = "postgresql+psycopg2"


SETTINGS = _Settings()