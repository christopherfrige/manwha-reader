from src.domain.entities.alternative_name import AlternativeName
from src.domain.entities.manwha import Manwha
from src.domain.entities.chapter import Chapter
from src.domain.schemas.manwha import (
    ManwhaPresentationData,
    GetManwhasResponse,
)
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.pagination.prepare_pagination import (
    PreparePaginationUseCase,
)
from src.domain.use_cases.pagination.get_limit_offset import (
    GetLimitOffsetUseCase,
)
from sqlalchemy.sql import func
from sqlalchemy import or_


class GetManwhasUseCase:
    def __init__(self, db: UnitOfWork):
        self.db = db
        self.get_limit_offset = GetLimitOffsetUseCase().execute
        self.prepare_pagination = PreparePaginationUseCase().execute

    def execute(self, search: str, page: int, per_page: int) -> GetManwhasResponse:
        with self.db.get_session() as session:
            limit, offset = self.get_limit_offset(page, per_page)

            subquery = (
                session.query(Chapter.id)
                .filter(Manwha.id == Chapter.manwha_id)
                .order_by(Chapter.chapter_number.desc())
                .limit(1)
                .correlate(Manwha)
            )

            query = (
                session.query(
                    func.max(Manwha.id).label("manwha_id"),
                    func.max(Manwha.name).label("manwha_name"),
                    func.max(Manwha.thumbnail).label("thumbnail"),
                    func.max(Chapter.id).label("last_chapter_id"),
                    func.max(Chapter.chapter_number).label("last_chapter_number"),
                    func.max(Chapter.created_at).label("last_chapter_uploaded_at"),
                )
                .join(Chapter, Chapter.manwha_id == Manwha.id)
                .join(AlternativeName, AlternativeName.manwha_id == Manwha.id)
                .filter(Chapter.id == subquery.scalar_subquery())
            )

            if search:
                search_terms = search.split(" ")
                conditions = []
                for term in search_terms:
                    conditions.append(Manwha.name.ilike(f"%{term}%"))
                    conditions.append(AlternativeName.name.ilike(f"%{term}%"))
                query = query.filter(or_(*conditions))

            query = query.group_by(Manwha.id).order_by(func.max(Chapter.created_at).desc())
            result = query.limit(limit).offset(offset)

            manwhas = [ManwhaPresentationData(**dict(row._mapping)) for row in result]

            return GetManwhasResponse(
                records=manwhas,
                pagination=self.prepare_pagination("/v1/manwhas", query, page, per_page),
            )
