from sqlalchemy.orm import Session

from src.domain.entities.artist import Artist
from src.domain.repository import BaseRepository


class ArtistRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Artist)
