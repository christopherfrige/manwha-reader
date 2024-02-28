from pydantic import BaseModel

class ChapterSchema(BaseModel):
    id: int
    chapter_number: float