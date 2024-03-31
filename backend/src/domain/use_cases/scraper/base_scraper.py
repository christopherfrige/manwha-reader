from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from src.domain.use_cases.manwha.manage_manwha import ManageManwhaUseCase
from src.domain.use_cases.chapter.check_new_chapters import CheckNewChaptersUseCase
from src.domain.use_cases.chapter.manage_chapters import ManageChaptersUseCase
from src.domain.use_cases.common.download_image import DownloadImageUseCase
from src.domain.repository.scraper import ScraperManwhaRepository
from src.infrastructure.services.s3 import S3Service
from src.infrastructure.log import logger


class BaseScraperUseCase(ABC):
    def __init__(self, session, storage: S3Service):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.scraper = webdriver.Chrome(
            service=Service(executable_path="/var/www/manwha-reader/chromedriver"), options=options
        )

        self.session = session

        self.scraper_manwha_repository = ScraperManwhaRepository(session)

        self.manage_manwha = ManageManwhaUseCase(session, storage)
        self.manage_chapters = ManageChaptersUseCase(session, storage)
        self.check_new_chapters = CheckNewChaptersUseCase(session)
        self.download_image = DownloadImageUseCase()

    def execute(self):
        with self.scraper as scraper:
            self.scraper = scraper

            manwhas_to_scrape = self.scraper_manwha_repository.get("id", self.reader_id)
            for scrape_manwha in manwhas_to_scrape:
                try:
                    logger.info(f"Scraping manwha from URL: {scrape_manwha.url}")

                    manwha_data = self.scrape_manwha_data(scrape_manwha.url)
                    manwha_id = self.manage_manwha.execute(manwha_data)

                    if not scrape_manwha.manwha_id:
                        self.scraper_manwha_repository.update(
                            "id", scrape_manwha.id, {"manwha_id": manwha_id}
                        )

                    self.session.commit()

                    new_chapters = self.check_new_chapters.execute(
                        manwha_id, manwha_data["chapters"]
                    )
                    if not new_chapters:
                        continue

                    for chapter in new_chapters:
                        try:
                            logger.info(
                                f"Scraping chapter {chapter['number']} from manwha {manwha_data['manwha_name']}"
                            )

                            chapter_pages = self.scrape_manwha_chapter_images(chapter["url"])
                            self.manage_chapters.execute(
                                manwha_id, chapter["number"], chapter_pages
                            )
                            self.session.commit()
                        except Exception as error:
                            self.session.rollback()
                            logger.exception(error)
                            continue
                except Exception as error:
                    self.session.rollback()
                    logger.exception(error)
                    continue

    def _remove_leading_trailing_whitespaces(self, data: str | list[str]) -> str | list[str]:
        if type(data) is str:
            return data.strip()
        return [item.strip() for item in data]

    @abstractmethod
    def scrape_manwha_data(self, manwha_url):
        pass

    @abstractmethod
    def scrape_manwha_chapter_images(self, chapter_url):
        pass
