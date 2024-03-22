from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.infrastructure.services.s3 import S3Service


class BaseScraper(ABC):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self.scraper = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    @abstractmethod
    def scrape_data(self):
        pass

    def run(self):
        with self.scraper as scraper:
            manwha_data = self.scrape_data(scraper)
            print(manwha_data)

    def check_if_exists(self):
        ...

    def save_chapter_images(self, localPath, remotePath):
        S3Service().upload_object(localPath, remotePath)
