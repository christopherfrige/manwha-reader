from src.domain.repository import BaseRepository
from src.domain.entities.manwha import Manwha


class ManwhaRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Manwha)


if __name__ == "__main__":
    print(ManwhaRepository()._get_all())
