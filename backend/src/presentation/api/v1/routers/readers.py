from fastapi import APIRouter, Depends

from src.domain.schemas.scraper import GetReadersResponse
from src.domain.use_cases.scraper.get_readers import GetReadersUseCase
from src.infrastructure.persistence.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/v1/readers", tags=["v1"])


@router.get("/", response_model=GetReadersResponse, status_code=200)
def get_chapter_pages(db=Depends(UnitOfWork)):
    return GetReadersUseCase(db).execute()
