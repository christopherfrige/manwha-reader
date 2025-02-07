from sqlalchemy.orm import Session

from src.domain.entities.author import Author
from src.domain.repository import BaseRepository


class AuthorRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Author)
