from src.domain.repository import BaseRepository
from src.domain.entities.artist import Artist
from sqlalchemy.orm import Session


class ArtistRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Artist)
