from src.domain.exceptions.client import NotFoundException
from src.domain.schemas.scraper import GetReadersResponse, ScraperManwhaSchema
from src.domain.repository.scraper import ScraperManwhaRepository
from src.infrastructure.persistence.unit_of_work import UnitOfWork


class GetScraperManwhaUseCase:
    def __init__(self, db: UnitOfWork):
        with db.get_session() as session:
            self.session = session
            self.scraper_manwha_repository = ScraperManwhaRepository(session)

    def execute(self, manwha_id: int) -> GetReadersResponse:
        scraper_manwha = self.scraper_manwha_repository.get("manwha_id", manwha_id).first()

        if not scraper_manwha:
            raise NotFoundException("The provided manwha_id was not found")

        return ScraperManwhaSchema(**scraper_manwha.to_dict())
