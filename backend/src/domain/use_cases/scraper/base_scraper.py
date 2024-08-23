from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from sqlalchemy.orm import Session
from src.domain.use_cases.manwha.manage_manwha import ManageManwhaUseCase
from src.domain.use_cases.chapter.check_new_chapters import CheckNewChaptersUseCase
from src.domain.use_cases.chapter.manage_chapters import ManageChaptersUseCase
from src.domain.use_cases.common.download_image import DownloadImageUseCase
from src.domain.repository.scraper import ScraperManwhaRepository
from src.infrastructure.services.s3 import S3Service
from src.infrastructure.log import logger


class BaseScraperUseCase(ABC):
    def __init__(self, session: Session, storage: S3Service, scraper_manwha_id: int | None):
        self.session = session
        self.scraper_manwha_id = scraper_manwha_id

        self.scraper_manwha_repository = ScraperManwhaRepository(session)

        self.manage_manwha = ManageManwhaUseCase(session, storage)
        self.manage_chapters = ManageChaptersUseCase(session, storage)
        self.check_new_chapters = CheckNewChaptersUseCase(session)
        self.download_image = DownloadImageUseCase(self.referer)

    def _scraper_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def _init_scraper(self):
        self.scraper = webdriver.Chrome(
            service=Service(executable_path="/var/www/manwha-reader/chromedriver"),
            options=self._scraper_options(),
        )
        self.scraper.set_page_load_timeout(30)

    def execute(self):
        self._init_scraper()

        logger.info(f"Starting scraping from reader_id {self.reader_id}")

        if self.scraper_manwha_id:
            manwhas_to_scrape = self.scraper_manwha_repository.get(
                "id", self.scraper_manwha_id
            ).all()
        else:
            manwhas_to_scrape = self.scraper_manwha_repository.get(
                "reader_id", self.reader_id
            ).all()

        with self.scraper as scraper:
            self.scraper = scraper
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
                        logger.info("No new chapters")
                        continue

                    for chapter in new_chapters:
                        try:
                            logger.info(
                                f"Scraping chapter {chapter['number']} from manwha {manwha_data['manwha_name']}"
                            )

                            chapter_pages = self.scrape_manwha_chapter_images(chapter["url"])

                            self.manage_chapters.execute(
                                manwha_id, chapter["number"], chapter_pages, chapter["url"]
                            )
                            self.session.commit()
                        except TimeoutException:
                            logger.error(
                                f"Timeout when trying to scrape chapter {chapter['number']}"
                            )
                        except Exception:
                            self.session.rollback()
                            logger.exception(f"Error when scraping chapter {chapter['number']}")
                except TimeoutException:
                    logger.error("Timeout when trying to scrape manwha")
                except Exception:
                    self.session.rollback()
                    logger.exception("Error when scraping manwha")
        logger.info(f"End of scraping from reader_id {self.reader_id}")

    def _format_and_make_unique(self, data: str | list[str]) -> str | list[str]:
        if type(data) is str:
            return data.strip()
        return list(set([item.strip() for item in data]))

    @abstractmethod
    def scrape_manwha_data(self, manwha_url):
        pass

    @abstractmethod
    def scrape_manwha_chapter_images(self, chapter_url):
        pass
