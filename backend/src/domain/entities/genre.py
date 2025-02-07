from sqlalchemy import TIMESTAMP, Column, Integer, Text
from sqlalchemy.sql.functions import now

from src.domain.entities import Base


class GenreSchema:
    __table_args__ = {"schema": "genre"}


class Genre(Base, GenreSchema):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, default=now())
