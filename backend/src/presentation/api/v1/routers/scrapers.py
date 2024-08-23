from fastapi import APIRouter, Depends, BackgroundTasks
from src.domain.use_cases.scraper.update_scraper_manwha import UpdateScraperManwhaUseCase
from src.domain.use_cases.scraper.create_manwha_to_scrape import CreateManwhaToScrapeUseCase
from src.domain.schemas.scraper import (
    CreateManwhaToScrapeRequest,
    CreateManwhaToScrapeResponse,
    ScrapeManwhaRequest,
    ScraperManwhaSchema,
    UpdateScraperManwhaRequest,
)
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.services.s3 import S3Service
from src.domain.use_cases.scraper.get_scraper_manwha import GetScraperManwhaUseCase
from src.domain.use_cases.scraper.scrape_inari_manwhas import ScrapeInariManwhasUseCase
from src.domain.use_cases.scraper.scrape_flower_manwhas import (
    ScrapeFlowerManwhasUseCase,
)
from src.domain.use_cases.scraper.scrape_kingofshojo_manwhas import ScrapeKingOfShojoManwhasUseCase
from src.domain.use_cases.scraper.scrape_kun_manwhas import ScrapeKunManwhasUseCase
from src.domain.use_cases.scraper.scrape_miau_manwhas import ScrapeMiauManwhasUseCase


router = APIRouter(prefix="/api/v1/scrapers", tags=["v1"])


@router.post("/scrape", status_code=202)
async def scrape_manwha(
    background_tasks: BackgroundTasks,
    payload: ScrapeManwhaRequest,
    db=Depends(UnitOfWork),
    storage=Depends(S3Service),
):
    with db.get_session() as session:
        match payload.reader_id:
            case 1:
                use_case = ScrapeInariManwhasUseCase(session, storage, payload.scraper_manwha_id)
            case 2:
                use_case = ScrapeFlowerManwhasUseCase(session, storage, payload.scraper_manwha_id)
            case 3:
                use_case = ScrapeKunManwhasUseCase(session, storage, payload.scraper_manwha_id)
            case 4:
                use_case = ScrapeKingOfShojoManwhasUseCase(
                    session, storage, payload.scraper_manwha_id
                )
            case 5:
                use_case = ScrapeMiauManwhasUseCase(session, storage, payload.scraper_manwha_id)
        background_tasks.add_task(use_case.execute)
    return {"message": "Scraping request received"}


@router.get("/manwha/{manwha_id}", response_model=ScraperManwhaSchema)
async def get_scraper_manwha(manwha_id: int, db=Depends(UnitOfWork)):
    return GetScraperManwhaUseCase(db).execute(manwha_id)


@router.post("/manwha", response_model=CreateManwhaToScrapeResponse, status_code=201)
async def create_manwha_to_scrape(payload: CreateManwhaToScrapeRequest, db=Depends(UnitOfWork)):
    return CreateManwhaToScrapeUseCase(db).execute(payload)


@router.patch("/manwha/{manwha_id}", response_model=ScraperManwhaSchema)
async def update_scraper_manwha(
    manwha_id: int, payload: UpdateScraperManwhaRequest, db=Depends(UnitOfWork)
):
    return UpdateScraperManwhaUseCase(db).execute(manwha_id, payload)
