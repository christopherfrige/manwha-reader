import scrapy


class CustomImagesItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class FlowermangaSpider(scrapy.Spider):
    name = "flowermanga"
    allowed_domains = ["flowermanga.com"]
    start_urls = ["https://flowermanga.com/manga/como-se-o-amor-nao-existisse/capitulo-02/"]

    def parse(self, response):
        images = CustomImagesItem()
        images["image_urls"] = []

        for image in response.css(".wp-manga-chapter-img"):
            images["image_urls"].append(image.attrib["src"].replace("\t", "").replace("\n", ""))
        yield images

        # next_page = response.css('.next_page ::attr(href)').get()

        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
