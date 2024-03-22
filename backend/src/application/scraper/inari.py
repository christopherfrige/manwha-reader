from selenium.webdriver.common.by import By

import requests

from src.application.scraper import BaseScraper


class InariScraper(BaseScraper):
    def scrape_data(self, scraper):
        scraper.get("")

        raw_manwha_data = scraper.find_elements(By.CLASS_NAME, "imptdt")
        manwha_data = {}
        for data in raw_manwha_data:
            data = data.text.splitlines()
            manwha_data.update({data[0]: data[1]})

        return {
            "manwha_name": scraper.find_element(By.CLASS_NAME, "entry-title").text,
            "alternative_names": scraper.find_element(By.CLASS_NAME, "alternative").text.split(
                ","
            ),
            "thumbnail": scraper.find_element(By.CLASS_NAME, "attachment-").get_attribute("src"),
            "authors": manwha_data.get("Autor", "").split(","),
            "artists": manwha_data.get("Artista", "").split(","),
            "status": manwha_data.get("Estado"),
            "release": manwha_data.get("Lanzado"),
            "chapters": self.get_chapters(),
        }

    def get_chapters(self):
        chapters_raw = self.scraper.find_elements(By.CLASS_NAME, "eph-num")
        chapters = []
        for position, chapter in enumerate(chapters_raw):
            if position == 0:
                continue

            chapter_link = chapter.find_element(By.TAG_NAME, "a").get_attribute("href")
            chapter_number = chapter.find_element(By.CLASS_NAME, "chapternum").text
            formatted_chapter_number = chapter_number[-3:].replace(" ", "").replace("o", "")

            chapters.append({"url": chapter_link, "number": formatted_chapter_number})
        return chapters

    def get_chapter_images(self, chapter_url):
        self.scraper.get(chapter_url)
        elements = self.scraper.find_elements(By.CLASS_NAME, "ts-main-image")

        for image_position, html_tag in enumerate(elements):
            image_name = str(image_position).rjust(3, "0")
            image_url = html_tag.get_attribute("src")
            image_type = image_url.split(".")[-1]

            with open(f"{image_name}.{image_type}", "wb") as image:
                image.write(requests.get(image_url).content)


if __name__ == "__main__":
    InariScraper().run()
