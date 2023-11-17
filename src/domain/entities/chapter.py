from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Float
from src.domain.entities import Base
from sqlalchemy.orm import relationship

class ChapterSchema:
    __table_args__ = {"schema": "chapter"}

class Chapter(Base, ChapterSchema):
    __tablename__ = 'chapter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    manwha_id = Column(Integer, ForeignKey('manwha.id'), nullable=False)
    chapter_number = Column(Float, nullable=False)
    pages = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP)
    manwha = relationship('Manwha')