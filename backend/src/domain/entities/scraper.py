from sqlalchemy import Boolean, Column, Integer, Text, TIMESTAMP, ForeignKey
from src.domain.entities import Base
from sqlalchemy.sql.functions import now


class ScraperSchema:
    __table_args__ = {"schema": "scraper"}


class Reader(Base, ScraperSchema):
    __tablename__ = "reader"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, default=now())


class ScraperManwha(Base, ScraperSchema):
    __tablename__ = "manwha"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reader_id = Column(
        Integer,
        ForeignKey("scraper.reader.id"),
        primary_key=True,
        nullable=False,
    )
    manwha_id = Column(
        Integer,
        ForeignKey("manwha.manwha.id"),
        primary_key=True,
        nullable=True,
    )
    url = Column(Text, nullable=False)
    chapter_start = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, default=now())
