from sqlalchemy import Column, Integer, TIMESTAMP, Text
from src.domain.entities import Base

class ArtistSchema:
    __table_args__ = {"schema": "artist"}

class Artist(Base, ArtistSchema):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP)