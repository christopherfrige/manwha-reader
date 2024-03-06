from pydantic import BaseModel
from datetime import datetime

class ChapterSchema(BaseModel):
    id: int
    chapter_number: float
    created_at: datetime