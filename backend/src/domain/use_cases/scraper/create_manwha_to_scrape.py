from src.domain.entities.scraper import ScraperManwha
from src.domain.exceptions.client import BadRequestException, ConflictException
from src.domain.repository.scraper import (
    ReaderRepository,
    ScraperManwhaRepository,
)
from src.domain.schemas.scraper import (
    CreateManwhaToScrapeRequest,
    CreateManwhaToScrapeResponse,
)
from src.infrastructure.persistence.unit_of_work import UnitOfWork


class CreateManwhaToScrapeUseCase:
    def __init__(self, db: UnitOfWork) -> None:
        with db.get_session() as session:
            self.session = session
            self.reader_repository = ReaderRepository(session)
            self.scraper_manwha_repository = ScraperManwhaRepository(session)

    def execute(self, payload: CreateManwhaToScrapeRequest):
        reader = self.reader_repository.get("id", payload.reader_id).first()
        if not reader:
            raise BadRequestException("The provided reader_id was not found in database")

        manwha = self.scraper_manwha_repository.get("url", payload.url).first()
        if manwha:
            raise ConflictException("A manwha is already registered with the provided url")

        scraper_manwha_id = self.scraper_manwha_repository.add(
            ScraperManwha(
                reader_id=payload.reader_id,
                url=payload.url,
                chapter_start=payload.chapter_start,
            )
        )

        self.session.commit()

        return CreateManwhaToScrapeResponse(
            message="Manwha created and ready to be scraped",
            scraper_manwha_id=scraper_manwha_id,
        )
