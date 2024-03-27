from src.domain.repository import BaseRepository
from src.domain.entities.chapter import Chapter
from sqlalchemy.orm import Session


class ChapterRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Chapter)
