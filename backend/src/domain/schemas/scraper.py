from pydantic import BaseModel

from src.domain.schemas import Pagination


class ReaderData(BaseModel):
    id: int
    name: str


class GetReadersResponse(BaseModel):
    records: list[ReaderData]
    pagination: Pagination