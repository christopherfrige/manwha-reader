from sqlalchemy.orm import Session

from src.domain.entities.manwha import (
    Manwha,
    ManwhaArtist,
    ManwhaAuthor,
    ManwhaGenre,
)
from src.domain.repository import BaseRepository


class ManwhaRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Manwha)


class ManwhaAuthorRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ManwhaAuthor)


class ManwhaArtistRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ManwhaArtist)


class ManwhaGenreRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ManwhaGenre)
