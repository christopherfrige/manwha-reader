from src.application.manwha_scraper.manwha_scraper.spiders.flowermanga import FlowermangaSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Scraper:
    def __init__(self):
        settings_file_path = 'src.application.scraper.scraper.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = FlowermangaSpider # The spider you want to crawl

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()  # the script will block here until the crawling is finished

if __name__ == "__main__":
    scraper = Scraper()
    scraper.run_spiders()