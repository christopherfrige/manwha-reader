from src.domain.repository import BaseRepository
from src.domain.entities.alternative_name import AlternativeName
from sqlalchemy.orm import Session


class AlternativeNameRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, AlternativeName)
