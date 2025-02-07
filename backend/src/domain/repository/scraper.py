from sqlalchemy.orm import Session

from src.domain.entities.scraper import Reader, ScraperManwha
from src.domain.repository import BaseRepository


class ScraperManwhaRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ScraperManwha)


class ReaderRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Reader)
