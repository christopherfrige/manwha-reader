from src.domain.repository import BaseRepository
from src.domain.entities.genre import Genre
from sqlalchemy.orm import Session


class GenreRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Genre)
