from fastapi import APIRouter, Depends

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.get_all_manwhas import GetAllManwhasUseCase

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/manwhas")
def get_all_manwhas(db: UnitOfWork = Depends(UnitOfWork), page: int = 1, per_page: int = 100): #-> GetAllManwhasResponse
    manwhas = GetAllManwhasUseCase().execute(db)
    for manwha in manwhas:
        print(manwha.id)
    return {}
