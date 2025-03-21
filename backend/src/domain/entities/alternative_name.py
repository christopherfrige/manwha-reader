from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Text
from sqlalchemy.sql.functions import now

from src.domain.entities import Base


class AlternativeNameSchema:
    __table_args__ = {"schema": "alternative_name"}


class AlternativeName(Base, AlternativeNameSchema):
    __tablename__ = "alternative_name"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    manwha_id = Column(Integer, ForeignKey("manwha.manwha.id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, default=now())
