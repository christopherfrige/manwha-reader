from src.domain.repository import BaseRepository
from src.domain.entities.scraper import ScraperManwha, Reader
from sqlalchemy.orm import Session


class ScraperManwhaRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ScraperManwha)

class ReaderRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Reader)
