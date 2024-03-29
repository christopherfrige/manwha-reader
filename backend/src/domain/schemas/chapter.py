from pydantic import BaseModel
from datetime import datetime


class ChapterSchema(BaseModel):
    id: int
    chapter_number: float
    created_at: datetime


class ChapterPage(BaseModel):
    url: str


class GetChapterPagesResponse(BaseModel):
    manwha_id: int
    manwha_name: str
    chapter_number: float
    pages: list[ChapterPage]
