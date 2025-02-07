from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.sql.functions import now

from src.domain.entities import Base


class ChapterSchema:
    __table_args__ = {"schema": "chapter"}


class Chapter(Base, ChapterSchema):
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    manwha_id = Column(Integer, ForeignKey("manwha.manwha.id"), nullable=False)
    chapter_number = Column(Float, nullable=False)
    pages = Column(Integer, nullable=False)
    origin_url = Column(Text, nullable=True)
    downloaded = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, default=now())
