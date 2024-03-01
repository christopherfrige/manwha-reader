from src.domain.entities.manwha import Manwha, ManwhaChapter
from src.domain.entities.chapter import Chapter
from src.domain.schemas.manwha import ManwhaPresentationData, GetAllManwhasResponse
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.pagination.prepare_pagination import PreparePaginationUseCase
from src.domain.use_cases.pagination.get_limit_offset import GetLimitOffsetUseCase
from sqlalchemy.sql import func
from sqlalchemy import cast, String


class GetAllManwhasUseCase:
    def __init__(self):
        self.get_limit_offset = GetLimitOffsetUseCase().execute
        self.prepare_pagination = PreparePaginationUseCase().execute

    def execute(self, db: UnitOfWork, page: int, per_page: int) -> GetAllManwhasResponse:
        with db.get_session() as session:
            limit, offset = self.get_limit_offset(page, per_page)

            subquery = (
                session.query(Chapter.id)
                .filter(Manwha.id == ManwhaChapter.manwha_id)
                .filter(Chapter.id == ManwhaChapter.chapter_id)
                .order_by(Chapter.id.desc())
                .limit(1)
                .correlate(Manwha)
            )

            query = (
                session.query(
                    func.max(Manwha.id).label('manwha_id'),
                    func.max(Manwha.name).label('manwha_name'),
                    func.max(Manwha.thumbnail).label('thumbnail'),
                    func.max(Chapter.chapter_number).label('last_chapter'),
                    func.max(cast(Chapter.created_at, String)).label('last_chapter_uploaded_at')
                )
                .join(ManwhaChapter, Manwha.id == ManwhaChapter.manwha_id)
                .join(Chapter, Chapter.id == ManwhaChapter.chapter_id)
                .filter(Chapter.id == subquery.scalar_subquery())
                .group_by(Manwha.id)
                .order_by(func.max(Chapter.created_at).desc())
            ) 

            result = query.limit(limit).offset(offset)

            manwhas = [ManwhaPresentationData(**dict(row._mapping)) for row in result]
            
            return GetAllManwhasResponse(
                records=manwhas,
                pagination=self.prepare_pagination("/v1/manwhas", query, page, per_page)
            )


