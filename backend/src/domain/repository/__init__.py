from abc import ABC
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from sqlalchemy import update


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

    def add(self, obj: object) -> int | None:
        self.session.add(obj)
        self.session.flush()
        if hasattr(obj, "id"):
            return obj.id

    def update(
        self,
        where_field: str,
        where_value: str | int | float | bool,
        values_to_update: dict,
    ) -> None:
        where_field = getattr(self.model, where_field)
        query = update(self.model).where(where_field == where_value).values(**values_to_update)
        self.session.execute(query)

    def delete(self, obj: object) -> None:
        self.session.delete(obj)
