from fastapi import APIRouter, Depends, BackgroundTasks

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.services.s3 import S3Service
from src.domain.use_cases.scraper.scrape_inari_manwhas import ScrapeInariManwhasUseCase


router = APIRouter(prefix="/api/v1/scrapers", tags=["v1"])


@router.post("/inari", status_code=202)
def scrape_inari(
    background_tasks: BackgroundTasks, db=Depends(UnitOfWork), storage=Depends(S3Service)
):
    with db.get_session() as session:
        use_case = ScrapeInariManwhasUseCase(session, storage)
        background_tasks.add_task(use_case.execute)
    return {"message": "Scraping request received"}
