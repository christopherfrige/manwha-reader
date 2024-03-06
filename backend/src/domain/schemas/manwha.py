from pydantic import BaseModel
from src.domain.schemas import Pagination
from src.domain.schemas.artist import ArtistSchema
from src.domain.schemas.author import AuthorSchema
from src.domain.schemas.genre import GenreSchema
from src.domain.schemas.alternative_name import AlternativeNameSchema
from src.domain.schemas.chapter import ChapterSchema


class ManwhaPresentationData(BaseModel):
    manwha_id: int
    manwha_name: str
    thumbnail: str | None
    last_chapter_id: int
    last_chapter_number: float
    last_chapter_uploaded_at: str


class GetAllManwhasResponse(BaseModel):
    records: list[ManwhaPresentationData]
    pagination: Pagination


class GetManwhaResponse(BaseModel):
    name: str
    thumbnail: str
    chapters: list[ChapterSchema]
    genres: list[GenreSchema]
    alternative_names: list[AlternativeNameSchema]
    authors: list[AuthorSchema]
    artists: list[ArtistSchema]
