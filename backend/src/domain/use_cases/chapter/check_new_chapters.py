from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.chapter import Chapter
from src.domain.repository.chapter import ChapterRepository
from src.domain.repository.scraper import ScraperManwhaRepository


class CheckNewChaptersUseCase:
    def __init__(self, session: Session):
        self.session = session
        self.chapter_repository = ChapterRepository(session)
        self.scraper_manwha_repository = ScraperManwhaRepository(session)

    def execute(self, manwha_id: int, chapters_incoming: list):
        chapter_numbers_registered = self._get_chapters_numbers_registered(manwha_id)
        chapters_registered_not_downloaded = self._get_chapters_registered_and_not_downloaded(
            manwha_id
        )

        manwha = self.scraper_manwha_repository.get("manwha_id", manwha_id).first()
        if not manwha:
            raise Exception("Manwha not registered to scrape")

        chapter_ids_to_scrape = []
        for chapter_incoming in chapters_incoming:
            if chapter_incoming["number"] < manwha.chapter_start:
                continue
            chapter_registered_not_downloaded = [
                chapter_db
                for chapter_db in chapters_registered_not_downloaded
                if chapter_incoming["number"] == chapter_db["chapter_number"]
            ]
            if chapter_registered_not_downloaded:
                chapter_ids_to_scrape.append(chapter_registered_not_downloaded[0]["id"])
                continue
            if chapter_incoming["number"] not in chapter_numbers_registered:
                chapter_id = self._save_chapter_in_db(manwha_id, chapter_incoming)
                chapter_ids_to_scrape.append(chapter_id)

        self.session.commit()

        return chapter_ids_to_scrape

    def _save_chapter_in_db(self, manwha_id: int, chapter):
        return self.chapter_repository.add(
            Chapter(
                manwha_id=manwha_id,
                chapter_number=chapter["number"],
                pages=0,
                downloaded=False,
                origin_url=chapter["url"],
            )
        )

    def _get_chapters_numbers_registered(self, manwha_id: int):
        query = (
            select(Chapter.chapter_number)
            .filter(Chapter.manwha_id == manwha_id)
            .order_by(Chapter.chapter_number.desc())
        )
        return self.session.execute(query).scalars().all()

    def _get_chapters_registered_and_not_downloaded(self, manwha_id: int):
        query = (
            select(Chapter.id, Chapter.chapter_number)
            .filter(Chapter.manwha_id == manwha_id)
            .order_by(Chapter.chapter_number.desc())
            .filter(Chapter.downloaded == False)
        )
        chapters = self.session.execute(query).all()
        return [chapter._mapping for chapter in chapters]
