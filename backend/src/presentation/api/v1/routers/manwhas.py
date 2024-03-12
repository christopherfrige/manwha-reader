from fastapi import APIRouter, Depends

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.manwha.get_manwhas import GetManwhasUseCase
from src.domain.use_cases.manwha.get_manwha import GetManwhaUseCase
from src.domain.schemas.manwha import (
    GetManwhasResponse,
    GetManwhaResponse,
    SearchManwhasResponse,
)

router = APIRouter(prefix="/v1/manwhas", tags=["v1"])


@router.get("/", response_model=GetManwhasResponse, status_code=200)
def get_manwhas(
    order_by: str = "",
    order: str = "desc",
    search: str = "",
    page: int = 1,
    per_page: int = 20,
    db=Depends(UnitOfWork),
):
    return GetManwhasUseCase(db).execute(order_by, order, search, page, per_page)


@router.get("/{manwha_id}", response_model=GetManwhaResponse, status_code=200)
def get_manwha(manwha_id: int, db=Depends(UnitOfWork)):
    return GetManwhaUseCase().execute(db, manwha_id)
