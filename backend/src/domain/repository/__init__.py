from abc import ABC
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session


class BaseRepository(ABC):
    def __init__(self, session: Session, model: DeclarativeMeta):
        self.session = session
        self.model = model

    def get(self, field: str, value: str | int | float | bool) -> list:
        field = getattr(self.model, field)
        if type(value) is not list:
            value = [value]
        return self.session.query(self.model).where(field.in_(value)).all()

    def get_all(self) -> list:
        return self.session.query(self.model).all()

    def add(self, obj: object) -> None:
        self.session.add(obj)
        self.session.flush()
        if hasattr(obj, "id"):
            return obj.id

    def update(self, obj: object) -> None:
        self.session.merge(obj)

    def delete(self, obj: object) -> None:
        self.session.delete(obj)
