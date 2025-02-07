from fastapi import APIRouter, Depends

from src.domain.schemas.manwha import (
    GetManwhaResponse,
    GetManwhasRequestQueryParams,
    GetManwhasResponse,
)
from src.domain.use_cases.manwha.delete_manwha_chapters import (
    DeleteManwhaChaptersUseCase,
)
from src.domain.use_cases.manwha.get_manwha import GetManwhaUseCase
from src.domain.use_cases.manwha.get_manwhas import GetManwhasUseCase
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.services.s3 import S3Service

router = APIRouter(prefix="/api/v1/manwhas", tags=["v1"])


@router.get("/", response_model=GetManwhasResponse, status_code=200)
async def get_manwhas(
    query_params=Depends(GetManwhasRequestQueryParams),
    db=Depends(UnitOfWork),
):
    return GetManwhasUseCase(db).execute(query_params)


@router.get("/{manwha_id}", response_model=GetManwhaResponse, status_code=200)
async def get_manwha(manwha_id: int, db=Depends(UnitOfWork)):
    return GetManwhaUseCase().execute(db, manwha_id)


@router.delete("/{manwha_id}/chapters", status_code=200)
async def delete_manwha_chapters(
    manwha_id: int, db=Depends(UnitOfWork), storage=Depends(S3Service)
):
    return DeleteManwhaChaptersUseCase(db, storage).execute(manwha_id)
