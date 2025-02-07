from src.domain.exceptions.client import BadRequestException, NotFoundException
from src.domain.repository.scraper import ScraperManwhaRepository
from src.domain.schemas.scraper import (
    GetReadersResponse,
    ScraperManwhaSchema,
    UpdateScraperManwhaRequest,
)
from src.infrastructure.persistence.unit_of_work import UnitOfWork


class UpdateScraperManwhaUseCase:
    def __init__(self, db: UnitOfWork):
        with db.get_session() as session:
            self.session = session
            self.scraper_manwha_repository = ScraperManwhaRepository(session)

    def execute(self, manwha_id: int, payload: UpdateScraperManwhaRequest) -> GetReadersResponse:
        scraper_manwha = self.scraper_manwha_repository.get("manwha_id", manwha_id).first()

        if not scraper_manwha:
            raise NotFoundException("The provided manwha_id was not found")

        update_params = payload.model_dump(exclude_none=True)

        if not update_params:
            raise BadRequestException("No payload to update was provided")

        self.scraper_manwha_repository.update("manwha_id", manwha_id, update_params)
        self.session.commit()

        return ScraperManwhaSchema(**scraper_manwha.to_dict())
