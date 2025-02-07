from math import ceil

from sqlalchemy.orm.query import RowReturningQuery

from src.domain.schemas import Pagination


class PreparePaginationUseCase:
    @staticmethod
    def execute(
        endpoint: str,
        records: list | RowReturningQuery,
        current_page: int,
        per_page: int,
    ) -> Pagination:
        if type(records) is list:
            entries_quantity = len(records)
        else:
            entries_quantity = records.count()

        first_page = 1
        last_page = ceil(entries_quantity / per_page)
        next_page = current_page + 1 if current_page + 1 <= last_page else None
        prev_page = current_page - 1 if current_page - 1 > 0 else None

        first_url = f"{endpoint}?page={first_page}&per_page={per_page}"
        last_url = f"{endpoint}?page={last_page}&per_page={per_page}"
        next_url = f"{endpoint}?page={next_page}&per_page={per_page}" if next_page else None
        prev_url = f"{endpoint}?page={prev_page}&per_page={per_page}" if prev_page else None

        return Pagination(
            next=next_url,
            prev=prev_url,
            first=first_url,
            last=last_url,
            total=entries_quantity,
        )
