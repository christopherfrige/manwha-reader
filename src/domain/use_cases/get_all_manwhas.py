from src.domain.entities.manwha import Manwha
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from sqlalchemy import select


class GetAllManwhasUseCase:
    @staticmethod
    def execute(db: UnitOfWork, page: int, per_page:int):
        with db.get_session() as session:
            return (
                session
                .query(Manwha)
                .order_by(Manwha.id.desc())
                .limit()
            )
        
    
