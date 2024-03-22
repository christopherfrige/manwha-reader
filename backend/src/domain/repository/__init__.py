from abc import ABC
from sqlalchemy.ext.declarative import DeclarativeMeta
from src.infrastructure.persistence.unit_of_work import UnitOfWork


class BaseRepository(ABC):
    def __init__(self, model: DeclarativeMeta):
        self.db = UnitOfWork()
        self.model = model

    def _get(self, id: int) -> object:
        with self.db.get_session() as session:
            return session.query(self.model).filter_by(id=id).first()

    def _get_all(self) -> list:
        with self.db.get_session() as session:
            return session.query(self.model).all()

    def _add(self, obj: object) -> None:
        with self.db.get_session() as session:
            session.add(obj)
            session.commit()

    def _update(self, obj: object) -> None:
        with self.db.get_session() as session:
            session.merge(obj)
            session.commit()

    def _delete(self, obj: object) -> None:
        with self.db.get_session() as session:
            session.delete(obj)
            session.commit()
