from fastapi import APIRouter, Depends, BackgroundTasks
from src.domain.schemas.scraper import ScrapeManwhaRequest
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.services.s3 import S3Service
from src.domain.use_cases.scraper.scrape_inari_manwhas import ScrapeInariManwhasUseCase
from src.domain.use_cases.scraper.scrape_flower_manwhas import (
    ScrapeFlowerManwhasUseCase,
)
from src.domain.use_cases.scraper.scrape_kingofshojo_manwhas import ScrapeKingOfShojoManwhasUseCase
from src.domain.use_cases.scraper.scrape_kun_manwhas import ScrapeKunManwhasUseCase


router = APIRouter(prefix="/api/v1/scrapers", tags=["v1"])


@router.post("/scrape", status_code=202)
def scrape_manwha(
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
                use_case = ScrapeKingOfShojoManwhasUseCase(session, storage, payload.scraper_manwha_id)
        background_tasks.add_task(use_case.execute)
    return {"message": "Scraping request received"}
