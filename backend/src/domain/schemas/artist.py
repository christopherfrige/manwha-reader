from pydantic import BaseModel


class ArtistSchema(BaseModel):
    id: int
    name: str
