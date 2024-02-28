from sqlalchemy import Column, Integer, Text, TIMESTAMP
from src.domain.entities import Base


class GenreSchema:
    __table_args__ = {"schema": "genre"}


class Genre(Base, GenreSchema):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP)