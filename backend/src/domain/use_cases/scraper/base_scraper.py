from abc import ABC, abstractmethod
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from sqlalchemy.orm import Session
from src.domain.utils import normalize_string
from src.domain.entities.scraper import ScraperManwha
from src.domain.exceptions.client import BadRequestException, NotAcceptableException
from src.domain.entities.chapter import Chapter
from src.domain.repository.chapter import ChapterRepository
from src.domain.exceptions.server import BadGatewayException
from src.domain.use_cases.manwha.manage_manwha import ManageManwhaUseCase
from src.domain.use_cases.chapter.check_new_chapters import CheckNewChaptersUseCase
from src.domain.use_cases.chapter.upload_chapter_pages import UploadChapterPagesUseCase
from src.domain.use_cases.common.download_image import DownloadImageUseCase
from src.domain.repository.scraper import ScraperManwhaRepository
from src.infrastructure.services.s3 import S3Service
from src.infrastructure.log import logger


class BaseScraperUseCase(ABC):
    def __init__(
        self,
        session: Session,
        storage: S3Service,
    ):
        self.referer = None

        self.session = session

        self.scraper_manwha_repository = ScraperManwhaRepository(session)
        self.chapter_repository = ChapterRepository(session)

        self.manage_manwha = ManageManwhaUseCase(session, storage)
        self.upload_chapter_pages = UploadChapterPagesUseCase(session, storage)
        self.check_new_chapters = CheckNewChaptersUseCase(session)
        self.download_image = DownloadImageUseCase(self.referer)

    def _driver_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def _init_scraper(self):
        self.scraper = webdriver.Chrome(
            service=Service(executable_path="/var/www/manwha-reader/chromedriver"),
            options=self._driver_options(),
        )
        self.scraper.set_page_load_timeout(30)

    def _close_scraper(self):
        self.scraper.quit()

    def execute_manhwhas(self, scraper_manwha_id: int | None):
        logger.info(f"Start scraping from reader_id {self.reader_id}")

        self._init_scraper()

        scrape_just_one_manwha = scraper_manwha_id is not None
        if scrape_just_one_manwha:
            manwhas_to_scrape: list[ScraperManwha] = self.scraper_manwha_repository.get(
                "id", scraper_manwha_id
            ).all()
        else:
            manwhas_to_scrape: list[ScraperManwha] = (
                self.scraper_manwha_repository.get("reader_id", self.reader_id)
                .where(ScraperManwha.active)
                .all()
            )

        if not manwhas_to_scrape:
            raise BadRequestException("No manwhas actives with the provided params")

        manwha_ids_with_new_chapters = []
        for scrape_manwha in manwhas_to_scrape:
            try:
                logger.info(f"Scraping manwha from URL: {scrape_manwha.url}")

                manwha_data = self.scrape_manwha_main_page(scrape_manwha.url)
                manwha_id = self.manage_manwha.execute(manwha_data)

                if not scrape_manwha.manwha_id or not scrape_manwha.active:
                    self.scraper_manwha_repository.update(
                        "id", scrape_manwha.id, {"manwha_id": manwha_id, "active": True}
                    )
                    self.session.commit()

                new_chapters = self.check_new_chapters.execute(manwha_id, manwha_data["chapters"])
                if new_chapters:
                    manwha_ids_with_new_chapters.append(manwha_id)
                else:
                    logger.info("No new chapters")
                    if scrape_just_one_manwha:
                        raise NotAcceptableException("No new chapters")

            except NotAcceptableException:
                raise
            except TimeoutException:
                logger.error(f"Timeout when scraping manwha from URL: {scrape_manwha.url}")
                raise BadGatewayException(
                    "Timeout when acessing website to scrape. Try again later."
                )
            except Exception:
                self.session.rollback()
                logger.exception("Error when scraping manwha")

        logger.info(f"End of scraping from reader_id {self.reader_id}")
        return manwha_ids_with_new_chapters

    def execute_chapters(self, manwha_ids: list[int]) -> None:
        chapters_pages_to_scrape: list[Chapter] = (
            self.chapter_repository.get("manwha_id", manwha_ids)
            .filter(Chapter.downloaded == False)
            .order_by(Chapter.manwha_id.asc())
            .order_by(Chapter.chapter_number.asc())
            .all()
        )

        for chapter in chapters_pages_to_scrape:
            try:
                logger.info(
                    f"Scraping chapter {chapter.chapter_number} from manwha ID {chapter.manwha_id}"
                )

                chapter_pages = self.scrape_manwha_chapter_pages(chapter.origin_url)

                chapter_images_local_folder = f"/tmp/{normalize_string(chapter.origin_url)}"

                for chapter_page in chapter_pages:
                    self.download_image.execute(
                        local_dir=chapter_images_local_folder,
                        image_name=chapter_page["image_name"],
                        image_type=chapter_page["image_type"],
                        image_url=chapter_page["image_url"],
                    )

                self.upload_chapter_pages.execute(len(chapter_pages), chapter)

                shutil.rmtree(chapter_images_local_folder)

                self.session.commit()
            except TimeoutException:
                logger.error(
                    f"Timeout when scraping chapter {chapter.chapter_number}, finishing the scrape job"
                )
                continue
            except Exception:
                self.session.rollback()
                logger.exception(f"Error when scraping chapter {chapter.chapter_number}")

        self._close_scraper()
        logger.info("Finished scraping manwhas chapters")

    def _format_and_make_unique(self, data: str | list[str]) -> str | list[str]:
        if type(data) is str:
            return data.strip()
        return list(set([item.strip() for item in data]))

    @abstractmethod
    def scrape_manwha_main_page(self, manwha_url):
        pass

    @abstractmethod
    def scrape_manwha_chapter_pages(self, chapter_url):
        pass
