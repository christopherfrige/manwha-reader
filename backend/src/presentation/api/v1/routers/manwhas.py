from fastapi import APIRouter, Depends

from src.infrastructure.services.s3 import S3Service
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.manwha.delete_manwha_chapters import DeleteManwhaChaptersUseCase
from src.domain.use_cases.manwha.get_manwhas import GetManwhasUseCase
from src.domain.use_cases.manwha.get_manwha import GetManwhaUseCase
from src.domain.schemas.manwha import (
    GetManwhasResponse,
    GetManwhaResponse,
)

router = APIRouter(prefix="/api/v1/manwhas", tags=["v1"])


@router.get("/", response_model=GetManwhasResponse, status_code=200)
async def get_manwhas(
    search: str = "",
    page: int = 1,
    per_page: int = 20,
    db=Depends(UnitOfWork),
):
    return GetManwhasUseCase(db).execute(search, page, per_page)


@router.get("/{manwha_id}", response_model=GetManwhaResponse, status_code=200)
async def get_manwha(manwha_id: int, db=Depends(UnitOfWork)):
    return GetManwhaUseCase().execute(db, manwha_id)


@router.delete("/{manwha_id}/chapters", status_code=200)
async def delete_manwha_chapters(
    manwha_id: int, db=Depends(UnitOfWork), storage=Depends(S3Service)
):
    return DeleteManwhaChaptersUseCase(db, storage).execute(manwha_id)
