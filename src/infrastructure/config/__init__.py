from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    app_environment: str = "development"

    db_host: str = "localhost"
    db_user: str = "root"
    db_password: str = "password"
    db_port: str = "5433"
    db_name: str = "manwha"
    db_driver: str = "postgresql+psycopg2"


SETTINGS = _Settings()