from sqlalchemy import Boolean, Column, Integer, ForeignKey, TIMESTAMP, Float, Text
from src.domain.entities import Base
from sqlalchemy.sql.functions import now


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
