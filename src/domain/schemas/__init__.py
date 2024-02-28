from pydantic import BaseModel

class Pagination(BaseModel):
    next: str | None
    prev: str | None
    first: str | None
    last: str | None
    total: int