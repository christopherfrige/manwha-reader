from fastapi import APIRouter, Depends

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases import GetAllManwhasUseCase

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/manwhas")
def get_all_manwhas(db: UnitOfWork = Depends(UnitOfWork)):
    return GetAllManwhasUseCase().execute(db)
