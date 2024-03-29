from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from src.domain.entities import Base


class ManwhaSchema:
    __table_args__ = {"schema": "manwha"}


class Manwha(Base, ManwhaSchema):
    __tablename__ = "manwha"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    thumbnail = Column(Text)
    summary = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP)


class ManwhaChapter(Base, ManwhaSchema):
    __tablename__ = "manwha_chapter"

    manwha_id = Column(
        Integer,
        ForeignKey("manwha.manwha.id"),
        primary_key=True,
        nullable=False,
    )
    chapter_id = Column(
        Integer,
        ForeignKey("chapter.chapter.id"),
        primary_key=True,
        nullable=False,
    )


class ManwhaAlternativeName(Base, ManwhaSchema):
    __tablename__ = "manwha_alternative_name"

    manwha_id = Column(
        Integer,
        ForeignKey("manwha.manwha.id"),
        primary_key=True,
        nullable=False,
    )
    alternative_name_id = Column(
        Integer,
        ForeignKey("alternative_name.alternative_name.id"),
        primary_key=True,
        nullable=False,
    )


class ManwhaGenre(Base, ManwhaSchema):
    __tablename__ = "manwha_genre"

    manwha_id = Column(
        Integer,
        ForeignKey("manwha.manwha.id"),
        primary_key=True,
        nullable=False,
    )
    genre_id = Column(Integer, ForeignKey("genre.genre.id"), primary_key=True, nullable=False)


class ManwhaAuthor(Base, ManwhaSchema):
    __tablename__ = "manwha_author"

    manwha_id = Column(
        Integer,
        ForeignKey("manwha.manwha.id"),
        primary_key=True,
        nullable=False,
    )
    author_id = Column(
        Integer,
        ForeignKey("author.author.id"),
        primary_key=True,
        nullable=False,
    )


class ManwhaArtist(Base, ManwhaSchema):
    __tablename__ = "manwha_artist"

    manwha_id = Column(
        Integer,
        ForeignKey("manwha.manwha.id"),
        primary_key=True,
        nullable=False,
    )
    artist_id = Column(
        Integer,
        ForeignKey("artist.artist.id"),
        primary_key=True,
        nullable=False,
    )
