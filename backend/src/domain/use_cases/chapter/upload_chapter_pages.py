import os

from sqlalchemy.orm import Session

from src.domain.entities.chapter import Chapter
from src.domain.repository.chapter import ChapterRepository
from src.domain.utils import normalize_string
from src.infrastructure.services.s3 import S3Service


class UploadChapterPagesUseCase:
    def __init__(self, session: Session, storage: S3Service):
        self.session = session
        self.storage = storage
        self.chapter_repository = ChapterRepository(session)

    def execute(self, pages: int, chapter: Chapter):
        self._upload_chapter_pages(chapter)
        self.chapter_repository.update("id", chapter.id, {"downloaded": True, "pages": pages})

    def _upload_chapter_pages(self, chapter: Chapter):
        chapter_images_local_folder = f"/tmp/{normalize_string(chapter.origin_url)}"

        for image_name in os.listdir(chapter_images_local_folder):
            self.storage.upload_object(
                local_path=f"{chapter_images_local_folder}/{image_name}",
                storage_path=f"manwha/{chapter.manwha_id}/chapters/{chapter.id}/{image_name}",
            )
