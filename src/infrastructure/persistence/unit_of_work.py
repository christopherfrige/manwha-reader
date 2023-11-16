from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from src.infrastructure.config import SETTINGS


class UnitOfWork:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(
            f"{SETTINGS.db_driver}://{SETTINGS.db_user}:{SETTINGS.db_password}@{SETTINGS.db_host}:{SETTINGS.db_port}"
        )
        self.session = sessionmaker(bind=self.engine, autoflush=True, autocommit=False)

    @contextmanager
    def get_session(self):
        try:
            session = self.session()
            yield session
        except Exception as error:
            session.rollback()
            raise
        finally:
            session.close()
