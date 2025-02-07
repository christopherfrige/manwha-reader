from src.domain.entities.chapter import Chapter
from src.domain.entities.manwha import Manwha
from src.domain.schemas.chapter import ChapterPage, GetChapterPagesResponse
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.services.s3 import S3Service


class GetChapterPagesUseCase:
    def __init__(self, db: UnitOfWork):
        self.db = db
        self.storage = S3Service()

    def execute(self, chapter_id: int) -> GetChapterPagesResponse:
        with self.db.get_session() as session:
            result = (
                session.query(
                    Manwha.id.label("manwha_id"),
                    Manwha.name.label("manwha_name"),
                    Chapter.chapter_number.label("chapter_number"),
                    Chapter.pages.label("chapter_pages"),
                )
                .join(Chapter, Chapter.manwha_id == Manwha.id)
                .filter(Chapter.id == chapter_id, Chapter.downloaded)
            ).first()

            if not result:
                raise Exception

            return GetChapterPagesResponse(
                manwha_id=result.manwha_id,
                manwha_name=result.manwha_name,
                chapter_number=result.chapter_number,
                pages=self.prepare_chapter_pages(result.manwha_id, chapter_id),
            )

    def prepare_chapter_pages(self, manwha_id: int, chapter_id: int) -> list[ChapterPage]:
        chapter_pages = self.storage.list_objects(path=f"manwha/{manwha_id}/chapters/{chapter_id}/")
        return [ChapterPage(url=f"{self.storage.bucket_url}/{page}") for page in chapter_pages]
