from sqlalchemy.orm import Session

from src.domain.entities.alternative_name import AlternativeName
from src.domain.repository import BaseRepository


class AlternativeNameRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session, AlternativeName)
