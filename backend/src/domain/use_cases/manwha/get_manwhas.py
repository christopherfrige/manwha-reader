from sqlalchemy import asc, case, desc, or_
from sqlalchemy.sql import func

from src.domain.entities.alternative_name import AlternativeName
from src.domain.entities.chapter import Chapter
from src.domain.entities.manwha import Manwha
from src.domain.enums.core import OrdenationOrder
from src.domain.enums.manwha import GetManwhasOrderEntity
from src.domain.schemas.manwha import (
    GetManwhasRequestQueryParams,
    GetManwhasResponse,
    ManwhaPresentationData,
)
from src.domain.use_cases.pagination.get_limit_offset import (
    GetLimitOffsetUseCase,
)
from src.domain.use_cases.pagination.prepare_pagination import (
    PreparePaginationUseCase,
)
from src.infrastructure.persistence.unit_of_work import UnitOfWork


class GetManwhasUseCase:
    def __init__(self, db: UnitOfWork):
        self.db = db
        self.get_limit_offset = GetLimitOffsetUseCase().execute
        self.prepare_pagination = PreparePaginationUseCase().execute

    def execute(self, query_params: GetManwhasRequestQueryParams) -> GetManwhasResponse:
        with self.db.get_session() as session:
            limit, offset = self.get_limit_offset(query_params.page, query_params.per_page)

            subquery = session.query(Chapter.id).filter(Manwha.id == Chapter.manwha_id)
            if query_params.with_chapters_downloaded:
                subquery = subquery.filter(Chapter.downloaded == True)
            subquery = subquery.order_by(Chapter.chapter_number.desc()).limit(1).correlate(Manwha)

            downloaded_subquery = (
                session.query(func.count(Chapter.id))
                .filter(Chapter.manwha_id == Manwha.id)
                .filter(Chapter.downloaded == True)
                .correlate(Manwha)
            )

            query = (
                session.query(
                    func.max(Manwha.id).label("manwha_id"),
                    func.max(Manwha.name).label("manwha_name"),
                    func.max(Manwha.thumbnail).label("thumbnail"),
                    func.max(Chapter.id).label("last_chapter_id"),
                    func.max(Chapter.chapter_number).label("last_chapter_number"),
                    func.max(Chapter.updated_at).label("last_chapter_uploaded_at"),
                    case((downloaded_subquery.exists(), True), else_=False).label(
                        "has_chapters_downloaded"
                    ),
                )
                .join(Chapter, Chapter.manwha_id == Manwha.id, isouter=True)
                .join(
                    AlternativeName,
                    AlternativeName.manwha_id == Manwha.id,
                    isouter=True,
                )
                .filter(Chapter.id == subquery.scalar_subquery())
            )

            if query_params.search:
                search_conditions = self._get_search_conditions(query_params.search)
                query = query.filter(or_(*search_conditions))

            _order_by, _order = self._prepare_ordenation(
                query_params.order_entity,
                query_params.order_by,
                query_params.order,
            )
            query = query.group_by(Manwha.id, Chapter.downloaded)
            query = query.order_by(_order(func.max(_order_by)))

            result = query.limit(limit).offset(offset)

            manwhas = [ManwhaPresentationData(**dict(row._mapping)) for row in result]

            return GetManwhasResponse(
                records=manwhas,
                pagination=self.prepare_pagination(
                    "/v1/manwhas",
                    query,
                    query_params.page,
                    query_params.per_page,
                ),
            )

    def _get_search_conditions(self, search_input: str):
        search_terms = search_input.split(" ")
        conditions = []
        for term in search_terms:
            conditions.append(Manwha.name.ilike(f"%{term}%"))
            conditions.append(AlternativeName.name.ilike(f"%{term}%"))
        return conditions

    def _prepare_ordenation(
        self,
        order_entity: GetManwhasOrderEntity,
        order_by: str,
        order: OrdenationOrder,
    ):
        match order_entity:
            case GetManwhasOrderEntity.MANWHA:
                prepared_order_entity = Manwha
            case _:
                prepared_order_entity = Chapter

        prepared_order_by = getattr(prepared_order_entity, order_by)
        prepared_order = asc if order == OrdenationOrder.ASC else desc

        return prepared_order_by, prepared_order
