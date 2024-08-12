from sqlalchemy.orm import Session
from src.domain.use_cases.scraper.base_scraper import BaseScraperUseCase
from selenium.webdriver.common.by import By
from src.infrastructure.config import SETTINGS
from src.infrastructure.services.s3 import S3Service
from selenium.common.exceptions import NoSuchElementException


class ScrapeMiauManwhasUseCase(BaseScraperUseCase):
    def __init__(self, session: Session, storage: S3Service, scraper_manwha_id: int | None):
        self.reader_id = 5
        self.referer = None
        super().__init__(session, storage, scraper_manwha_id)

    def scrape_manwha_data(self, manwha_url: str):
        self.scraper.get(manwha_url)

        manwha_attributes = self._get_manwha_attributes()

        return {
            "manwha_name": self._get_manwha_name(),
            "alternative_names": self._get_alternative_names(),
            "summary": self._get_summary(),
            "thumbnail": self._get_thumbnail(),
            "genres": self._get_genres(),
            "authors": manwha_attributes["authors"],
            "artists": manwha_attributes["artists"],
            "release": manwha_attributes["release"],
            "chapters": self._get_chapters_numbers_and_urls(),
        }

    def scrape_manwha_chapter_images(self, chapter_url):
        self.scraper.get(chapter_url)

        elements = self.scraper.find_elements(By.CLASS_NAME, "ts-main-image")

        chapter_pages = 0
        for image_position, html_tag in enumerate(elements):
            image_url = html_tag.get_attribute("src")
            image_name = str(image_position).rjust(3, "0")
            image_type = image_url.split(".")[-1]

            self.download_image.execute(
                local_dir=SETTINGS.chapter_images_local_folder,
                image_name=image_name,
                image_type=image_type,
                image_url=image_url,
            )
            chapter_pages += 1

        return chapter_pages

    def _get_manwha_name(self) -> str:
        manwha_name = self.scraper.find_element(By.CLASS_NAME, "entry-title").get_attribute(
            "innerText"
        )
        return self._format_and_make_unique(manwha_name)

    def _get_thumbnail(self) -> str:
        thumbnail = self.scraper.find_element(By.CLASS_NAME, "attachment-").get_attribute("src")
        return thumbnail

    def _get_summary(self) -> str:
        summary = (
            self.scraper.find_element(By.CLASS_NAME, "entry-content")
            .find_element(By.TAG_NAME, "p")
            .get_attribute("innerText")
        )
        return summary

    def _get_alternative_names(self) -> list[str]:
        try:
            alternative_names = (
                self.scraper.find_element(By.CLASS_NAME, "alternative")
                .get_attribute("innerText")
                .split(",")
            )
            return self._format_and_make_unique(alternative_names)
        except NoSuchElementException:
            return []

    def _get_genres(self) -> list[str]:
        genres = [
            genre.get_attribute("innerText")
            for genre in self.scraper.find_element(By.CLASS_NAME, "mgen").find_elements(
                By.TAG_NAME, "a"
            )
        ]
        return self._format_and_make_unique(genres)

    def _get_manwha_attributes(self) -> dict:
        manwha_attributes = self.scraper.find_elements(By.CLASS_NAME, "imptdt")
        manwha_prepared_attributes = {}
        for attribute in manwha_attributes:
            attribute = attribute.get_attribute("innerText").splitlines()
            attribute_name = attribute[0]
            attribute_value = self._format_and_make_unique(attribute[1].split(","))
            manwha_prepared_attributes.update({attribute_name: attribute_value})

        return {
            "authors": manwha_prepared_attributes.get("Autor", []),
            "artists": manwha_prepared_attributes.get("Artista", []),
            "release": manwha_prepared_attributes.get("Lanzado", None),
        }

    def _get_chapters_numbers_and_urls(self):
        chapters_raw = self.scraper.find_elements(By.CLASS_NAME, "eph-num")
        chapters = []
        for position, chapter in enumerate(chapters_raw):
            if position == 0:
                continue

            chapter_link = chapter.find_element(By.TAG_NAME, "a").get_attribute("href")
            chapter_number = chapter.find_element(By.CLASS_NAME, "chapternum").get_attribute(
                "innerText"
            )
            formatted_chapter_number = float(chapter_number[8:].replace(" ", "").replace("o", ""))

            chapters.append({"url": chapter_link, "number": formatted_chapter_number})
        return chapters
