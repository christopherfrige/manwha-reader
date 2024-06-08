from src.domain.schemas.scraper import GetReadersResponse, ReaderData
from src.domain.repository.scraper import ReaderRepository
from src.domain.use_cases.pagination.prepare_pagination import PreparePaginationUseCase
from src.infrastructure.persistence.unit_of_work import UnitOfWork


class GetReadersUseCase:
    def __init__(self, db: UnitOfWork):
        with db.get_session() as session:
            self.session = session
            self.reader_repository = ReaderRepository(session)
            self.prepare_pagination = PreparePaginationUseCase().execute

    def execute(self) -> GetReadersResponse:
        readers = self.reader_repository.get_all()

        records = [ReaderData(id=reader.id, name=reader.name) for reader in readers]

        return GetReadersResponse(
            records=records,
            pagination=self.prepare_pagination("/v1/readers", query, page, per_page)
        )

