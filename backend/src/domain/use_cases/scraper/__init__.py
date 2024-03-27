from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from src.domain.use_cases.manwha.manage_manwha import ManageManwhaUseCase
from src.domain.use_cases.chapter.manage_chapters import ManageChaptersUseCase
from sqlalchemy.orm import Session


class BaseScraperUseCase(ABC):
    def __init__(self, session: Session):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        self.scraper = webdriver.Chrome(
            service=Service(executable_path="/var/www/manwha-reader/chromedriver"), options=options
        )

        self.manage_manwha = ManageManwhaUseCase(session)
        self.manage_chapters = ManageChaptersUseCase(session)

    @abstractmethod
    def scrape_manwha_data(self):
        pass

    @abstractmethod
    def scrape_manwha_chapter_images(self):
        pass

    def execute(self):
        with self.scraper as scraper:
            # manwha_data = self.scrape_manwha_data(scraper)
            manwha_id = self.manage_manwha.execute(manwha_data)
            self.manage_chapters.execute(manwha_id, manwha_data["chapters"])

    def check_if_exists(self):
        ...
