from src.domain.repository import BaseRepository
from src.domain.entities.author import Author
from sqlalchemy.orm import Session


class AuthorRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Author)
