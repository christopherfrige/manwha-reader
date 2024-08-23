from pydantic import BaseModel

from src.domain.schemas import Pagination


class ReaderData(BaseModel):
    id: int
    name: str


class GetReadersResponse(BaseModel):
    records: list[ReaderData]
    pagination: Pagination


class ScrapeManwhaRequest(BaseModel):
    reader_id: int
    scraper_manwha_id: int | None = None


class CreateManwhaToScrapeRequest(BaseModel):
    reader_id: int
    url: str
    chapter_start: int


class CreateManwhaToScrapeResponse(BaseModel):
    message: str
    scraper_manwha_id: int


class ScraperManwhaSchema(BaseModel):
    id: int
    reader_id: int
    manwha_id: int | None = None
    url: str
    chapter_start: int


class UpdateScraperManwhaRequest(BaseModel):
    url: str | None = None
    chapter_start: int | None = None
