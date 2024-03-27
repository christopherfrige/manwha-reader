from sqlalchemy import Column, Integer, TIMESTAMP, Text
from src.domain.entities import Base
from sqlalchemy.sql.functions import now


class AuthorSchema:
    __table_args__ = {"schema": "author"}


class Author(Base, AuthorSchema):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, default=now())
