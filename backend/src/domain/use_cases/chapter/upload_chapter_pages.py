from src.domain.repository.chapter import ChapterRepository
from src.domain.entities.chapter import Chapter
from src.infrastructure.services.s3 import S3Service
from sqlalchemy.orm import Session
from src.infrastructure.config import SETTINGS
import os
import shutil


class UploadChapterPagesUseCase:
    def __init__(self, session: Session, storage: S3Service):
        self.session = session
        self.storage = storage
        self.chapter_repository = ChapterRepository(session)

    def execute(self, pages: int, origin_url: str):
        chapter = self.chapter_repository.get("origin_url", origin_url).first()
        if chapter:
            self.chapter_repository.update("id", chapter.id, {"downloaded": True, "pages": pages})
            self._upload_chapter_pages(chapter.manwha_id, chapter.id)

    def _upload_chapter_pages(self, manwha_id: int, chapter_id: int):
        for image in os.listdir(SETTINGS.chapter_images_local_folder):
            self.storage.upload_object(
                local_path=f"{SETTINGS.chapter_images_local_folder}/{image}",
                storage_path=f"manwha/{manwha_id}/chapters/{chapter_id}/{image}",
            )
        shutil.rmtree(SETTINGS.chapter_images_local_folder)
