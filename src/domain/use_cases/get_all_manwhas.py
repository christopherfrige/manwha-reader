from src.domain.entities.manwha import Manwha
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from sqlalchemy import select


class GetAllManwhasUseCase:
    def execute(self, db: UnitOfWork):
        with db.get_session() as session:
            statement = select(Manwha)
            return session.execute(statement).mappings().all()
