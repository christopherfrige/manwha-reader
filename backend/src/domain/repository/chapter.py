from sqlalchemy.orm import Session

from src.domain.entities.chapter import Chapter
from src.domain.repository import BaseRepository


class ChapterRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Chapter)
