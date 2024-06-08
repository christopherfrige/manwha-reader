from fastapi import APIRouter, Depends, Response

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.manwha.get_manwhas import GetManwhasUseCase
from src.domain.use_cases.manwha.get_manwha import GetManwhaUseCase
from src.domain.use_cases.manwha.create_manwha_to_scrape import CreateManwhaToScrapeUseCase
from src.domain.schemas.manwha import (
    GetManwhasResponse,
    GetManwhaResponse,
    CreateManwhaToScrapeRequest,
    CreateManwhaToScrapeResponse
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


@router.post("/", status_code=201)
async def create_manwha_to_scrape(
    payload: CreateManwhaToScrapeRequest,
    db=Depends(UnitOfWork)
):
    CreateManwhaToScrapeUseCase(db).execute(payload)
    return Response(status_code=201)