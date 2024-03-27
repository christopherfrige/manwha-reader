from fastapi import APIRouter, Depends

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.scraper.scrape_inari_manwhas import ScrapeInariManwhasUseCase


router = APIRouter(prefix="/api/v1/scrapers", tags=["v1"])


@router.post("/inari", status_code=200)
def scrape_inari(db=Depends(UnitOfWork)):
    with db.get_session() as session:
        try:
            ScrapeInariManwhasUseCase(session).execute()
            session.commit()
        except Exception as error:
            print(error)
            session.rollback()
    return {}
