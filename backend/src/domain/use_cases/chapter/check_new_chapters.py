from src.domain.repository.scraper import ScraperManwhaRepository
from src.domain.entities.chapter import Chapter
from sqlalchemy.orm import Session
from sqlalchemy import select


class CheckNewChaptersUseCase:
    def __init__(self, session: Session):
        self.session = session
        self.scraper_manwha_repository = ScraperManwhaRepository(session)

    def execute(self, manwha_id: int, chapters_incoming: list):
        chapters_registered = self._get_chapters_registered(manwha_id)

        manwha = self.scraper_manwha_repository.get("manwha_id", manwha_id).first()

        chapter_start = 0
        if manwha:
            chapter_start = manwha.chapter_start

        chapters_difference = len(chapters_incoming) - len(chapters_registered)
        if chapters_difference == 0:
            return []

        new_chapters = []
        for chapter in chapters_incoming:
            if chapter["number"] < chapter_start:
                continue
            if chapter["number"] not in chapters_registered:
                new_chapters.append(chapter)

        new_chapters.sort(key=self._chapter_sort_criteria)

        return new_chapters

    def _get_chapters_registered(self, manwha_id: int):
        query = (
            select(Chapter.chapter_number)
            .filter(Chapter.manwha_id == manwha_id)
            .order_by(Chapter.chapter_number.desc())
        )
        return self.session.execute(query).scalars().all()

    def _chapter_sort_criteria(self, chapter):
        return chapter["number"]
