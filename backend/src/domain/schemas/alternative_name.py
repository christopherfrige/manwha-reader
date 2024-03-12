from pydantic import BaseModel


class AlternativeNameSchema(BaseModel):
    id: int
    name: str
