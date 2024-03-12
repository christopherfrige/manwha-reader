import scrapy


class CustomImagesItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class VisorTMOSpider(scrapy.Spider):
    name = "visortmo"
    allowed_domains = ["https://visortmo.com"]
    start_urls = ["https://visortmo.com/viewer/00cb7d705654f129d000d4eff64a4ab7/cascade"]

    def parse(self, response):
        images = CustomImagesItem()
        images["image_urls"] = []

        for image in response.css(".wp-manga-chapter-img"):
            images["image_urls"].append(image.attrib["src"])
        yield images

        # next_page = response.css('.next_page ::attr(href)').get()

        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
