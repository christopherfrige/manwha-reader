from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy.orm import Session

from src.domain.enums.scraper import ReaderEnum
from src.domain.use_cases.scraper.base_scraper import BaseScraperUseCase
from src.infrastructure.services.s3 import S3Service


class ScrapeHariManwhasUseCase(BaseScraperUseCase):
    def __init__(self, session: Session, storage: S3Service):
        super().__init__(session, storage)
        self.reader_id = ReaderEnum.HARI.value

    def scrape_manwha_main_page(self, manwha_url: str):
        self.scraper.get(manwha_url)

        manwha_attributes = self._get_manwha_attributes()

        return {
            "manwha_name": self._get_manwha_name(),
            "alternative_names": manwha_attributes["alternative_names"],
            "summary": self._get_summary(),
            "thumbnail": self._get_thumbnail(),
            "genres": manwha_attributes["genres"],
            "authors": manwha_attributes["authors"],
            "artists": manwha_attributes["artists"],
            "release": manwha_attributes["release"],
            "chapters": self._get_chapters_numbers_and_urls(),
        }

    def scrape_manwha_chapter_pages(self, chapter_url):
        self.scraper.get(chapter_url)

        chapter_pages = self.scraper.find_elements(By.CLASS_NAME, "wp-manga-chapter-img")

        pages = []
        for image_position, html_tag in enumerate(chapter_pages):
            image_url = html_tag.get_attribute("src")
            image_name = str(image_position).rjust(3, "0")
            image_type = image_url.split(".")[-1]

            pages.append(
                {
                    "image_url": image_url,
                    "image_name": image_name,
                    "image_type": image_type,
                }
            )

        return pages

    def _get_manwha_attributes(self) -> dict:
        manwha_attributes = self.scraper.find_elements(By.CLASS_NAME, "post-content_item")

        manwha_prepared_attributes = {}
        for attribute in manwha_attributes:
            try:
                attribute_name = (
                    attribute.find_element(By.CLASS_NAME, "summary-heading")
                    .find_element(By.TAG_NAME, "h5")
                    .get_attribute("innerText")
                )
                attribute_value = attribute.find_element(
                    By.CLASS_NAME, "summary-content"
                ).get_attribute("innerText")
                manwha_prepared_attributes.update({attribute_name: attribute_value})
            except NoSuchElementException:
                continue

        alternative_names = (
            manwha_prepared_attributes["Alternative"].split("/")
            if manwha_prepared_attributes.get("Alternative")
            else []
        )

        genres = (
            manwha_prepared_attributes["Genre(s)"].split(",")
            if manwha_prepared_attributes.get("Genre(s)")
            else []
        )

        authors = (
            manwha_prepared_attributes["Author(s)"].split(",")
            if manwha_prepared_attributes.get("Author(s)")
            else []
        )

        artists = (
            manwha_prepared_attributes["Artist(s)"].split(",")
            if manwha_prepared_attributes.get("Artist(s)")
            else []
        )

        return {
            "alternative_names": self._format_and_make_unique(alternative_names),
            "genres": self._format_and_make_unique(genres),
            "authors": self._format_and_make_unique(authors),
            "artists": self._format_and_make_unique(artists),
            "release": None,
        }

    def _get_manwha_name(self) -> str:
        manwha_name = (
            self.scraper.find_element(By.CLASS_NAME, "post-title")
            .find_element(By.TAG_NAME, "h1")
            .get_attribute("innerText")
        )
        return self._format_and_make_unique(manwha_name)

    def _get_thumbnail(self) -> str:
        thumbnail = (
            self.scraper.find_element(By.CLASS_NAME, "summary_image")
            .find_element(By.TAG_NAME, "img")
            .get_attribute("src")
        )
        return thumbnail

    def _get_summary(self) -> str:
        summary = (
            self.scraper.find_element(By.CLASS_NAME, "summary__content")
            .find_elements(By.TAG_NAME, "p")[1]
            .get_attribute("innerText")
        )
        return summary

    def _get_chapters_numbers_and_urls(self):
        chapters_raw = self.scraper.find_elements(By.CLASS_NAME, "wp-manga-chapter")
        chapters = []
        for chapter in chapters_raw:
            chapter_content = chapter.find_element(By.TAG_NAME, "a")

            chapter_link = chapter_content.get_attribute("href")

            chapter_number = chapter_content.get_attribute("innerText").split("-")[0]

            formatted_chapter_number = float(
                chapter_number[8:].replace("l", "").replace("o", "").replace(" ", "")
            )

            chapters.append({"url": chapter_link, "number": formatted_chapter_number})
        return chapters
