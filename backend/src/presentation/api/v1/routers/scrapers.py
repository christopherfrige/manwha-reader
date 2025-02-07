from fastapi import APIRouter, BackgroundTasks, Depends

from src.domain.enums.scraper import ReaderEnum
from src.domain.exceptions.client import BadRequestException
from src.domain.schemas.scraper import (
    CreateManwhaToScrapeRequest,
    CreateManwhaToScrapeResponse,
    ScrapeManwhaRequest,
    ScraperManwhaSchema,
    UpdateScraperManwhaRequest,
)
from src.domain.use_cases.scraper.base_scraper import BaseScraperUseCase
from src.domain.use_cases.scraper.create_manwha_to_scrape import (
    CreateManwhaToScrapeUseCase,
)
from src.domain.use_cases.scraper.get_scraper_manwha import (
    GetScraperManwhaUseCase,
)
from src.domain.use_cases.scraper.scrape_flower_manwhas import (
    ScrapeFlowerManwhasUseCase,
)
from src.domain.use_cases.scraper.scrape_hari_manwhas import (
    ScrapeHariManwhasUseCase,
)
from src.domain.use_cases.scraper.scrape_inari_manwhas import (
    ScrapeInariManwhasUseCase,
)
from src.domain.use_cases.scraper.scrape_kingofshojo_manwhas import (
    ScrapeKingOfShojoManwhasUseCase,
)
from src.domain.use_cases.scraper.scrape_kun_manwhas import (
    ScrapeKunManwhasUseCase,
)
from src.domain.use_cases.scraper.scrape_miau_manwhas import (
    ScrapeMiauManwhasUseCase,
)
from src.domain.use_cases.scraper.update_scraper_manwha import (
    UpdateScraperManwhaUseCase,
)
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.services.s3 import S3Service

router = APIRouter(prefix="/api/v1/scrapers", tags=["v1"])


@router.post("/scrape", status_code=202)
async def scrape_manwha(
    background_tasks: BackgroundTasks,
    payload: ScrapeManwhaRequest,
    db=Depends(UnitOfWork),
    storage=Depends(S3Service),
):
    with db.get_session() as session:
        scrapers: dict[ReaderEnum, BaseScraperUseCase] = {
            ReaderEnum.INARI.value: ScrapeInariManwhasUseCase,
            ReaderEnum.FLOWER.value: ScrapeFlowerManwhasUseCase,
            ReaderEnum.KUN.value: ScrapeKunManwhasUseCase,
            ReaderEnum.KING_OF_SHOJO.value: ScrapeKingOfShojoManwhasUseCase,
            ReaderEnum.MIAU.value: ScrapeMiauManwhasUseCase,
            ReaderEnum.HARI.value: ScrapeHariManwhasUseCase,
        }

        selected_scraper = scrapers.get(payload.reader_id)
        if selected_scraper:
            scraper: BaseScraperUseCase = selected_scraper(session=session, storage=storage)

            chapter_ids = scraper.execute_manhwhas(payload.scraper_manwha_id)
            if chapter_ids:
                background_tasks.add_task(scraper.execute_chapters, chapter_ids)

            return {"message": "Scraping request received sucessfully"}

        raise BadRequestException("The provided reader_id is not valid.")


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
