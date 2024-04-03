from pydantic import BaseModel


class ChapterSchema(BaseModel):
    id: int
    chapter_number: float
    created_at: str


class ChapterPage(BaseModel):
    url: str


class GetChapterPagesResponse(BaseModel):
    manwha_id: int
    manwha_name: str
    chapter_number: float
    pages: list[ChapterPage]
