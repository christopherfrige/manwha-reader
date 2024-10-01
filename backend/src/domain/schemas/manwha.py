from pydantic import BaseModel
from src.domain.enums.manwha import GetManwhasOrderEntity
from src.domain.enums.core import OrdenationOrder
from src.domain.schemas import Pagination
from src.domain.schemas.artist import ArtistSchema
from src.domain.schemas.author import AuthorSchema
from src.domain.schemas.genre import GenreSchema
from src.domain.schemas.alternative_name import AlternativeNameSchema
from src.domain.schemas.chapter import ChapterSchema

from datetime import datetime


class ManwhaSchema(BaseModel):
    id: str
    name: str
    thumbnail: str | None


class ManwhaPresentationData(BaseModel):
    manwha_id: int
    manwha_name: str
    thumbnail: str | None
    last_chapter_id: int
    last_chapter_number: float
    last_chapter_uploaded_at: datetime
    has_chapters_downloaded: bool


class GetManwhasRequestQueryParams(BaseModel):
    search: str = ""
    page: int = 1
    per_page: int = 20
    order_entity: GetManwhasOrderEntity = GetManwhasOrderEntity.CHAPTER
    order_by: str = "updated_at"
    order: OrdenationOrder = OrdenationOrder.DESC


class GetManwhasResponse(BaseModel):
    records: list[ManwhaPresentationData]
    pagination: Pagination


class GetManwhaResponse(BaseModel):
    name: str
    thumbnail: str | None
    chapters: list[ChapterSchema]
    genres: list[GenreSchema]
    alternative_names: list[AlternativeNameSchema]
    authors: list[AuthorSchema]
    artists: list[ArtistSchema]
    release: str | None


class SearchManwhasResponse(BaseModel):
    records: list[ManwhaSchema]
    pagination: Pagination
