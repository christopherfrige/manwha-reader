from src.infrastructure.services.s3 import S3Service
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.repository.chapter import ChapterRepository


class DeleteManwhaChaptersUseCase:
    def __init__(self, db: UnitOfWork, storage: S3Service):
        with db.get_session() as session:
            self.storage = storage
            self.session = session
            self.chapter_repository = ChapterRepository(session)

    def execute(self, manwha_id: int):
        objects_deleted = self.storage.delete_objects(path=f"manwha/{manwha_id}/chapters")

        if objects_deleted:
            self.chapter_repository.update("manwha_id", manwha_id, {"downloaded": False})
            self.session.commit()
