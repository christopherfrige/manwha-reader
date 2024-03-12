from src.domain.entities.manwha import Manwha, ManwhaChapter
from src.domain.entities.chapter import Chapter
from src.domain.schemas.chapter import GetChapterPagesResponse, ChapterPage
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.config import SETTINGS


class GetChapterPagesUseCase:
    def __init__(self, db: UnitOfWork):
        self.db = db

    def execute(self, chapter_id: int) -> GetChapterPagesResponse:
        with self.db.get_session() as session:
            result = (
                session.query(
                    Manwha.id.label("manwha_id"),
                    Manwha.name.label("manwha_name"),
                    Chapter.chapter_number.label("chapter_number"),
                    Chapter.pages.label("chapter_pages"),
                )
                .join(ManwhaChapter, Manwha.id == ManwhaChapter.manwha_id)
                .join(Chapter, Chapter.id == ManwhaChapter.chapter_id)
                .filter(Chapter.id == chapter_id)
            ).first()

            if not result:
                raise Exception

            return GetChapterPagesResponse(
                manwha_id=result.manwha_id,
                manwha_name=result.manwha_name,
                chapter_number=result.chapter_number,
                pages=self.prepare_chapter_pages(chapter_id, result.chapter_pages),
            )

    def prepare_chapter_pages(self, chapter_id: int, chapter_pages: int) -> list[ChapterPage]:
        all_pages = range(1, chapter_pages + 1)
        return [
            ChapterPage(
                url=f"{SETTINGS.aws_bucket_url}/{chapter_id}/{page}.jpg",
            )
            for page in all_pages
        ]
