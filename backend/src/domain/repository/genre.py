from sqlalchemy.orm import Session

from src.domain.entities.genre import Genre
from src.domain.repository import BaseRepository


class GenreRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Genre)
