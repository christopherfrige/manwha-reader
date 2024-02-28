from fastapi import APIRouter, Depends

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.manwha.get_all_manwhas import GetAllManwhasUseCase
from src.domain.use_cases.manwha.get_manwha import GetManwhaUseCase
from src.domain.schemas.manwha import GetAllManwhasResponse, GetManwhaResponse

router = APIRouter(prefix="/v1/manwhas", tags=["v1"])


@router.get("/", response_model=GetAllManwhasResponse, status_code=200)
def get_all_manwhas(page: int = 1, per_page: int = 20, db = Depends(UnitOfWork)):
    return GetAllManwhasUseCase().execute(db, page, per_page)

@router.get("/{manwha_id}", response_model=GetManwhaResponse, status_code=200)
def get_manwha(manwha_id: int, db = Depends(UnitOfWork)):
    return GetManwhaUseCase().execute(db, manwha_id)
