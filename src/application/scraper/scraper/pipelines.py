# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline

class customImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image in item['image_urls']:
            yield Request(image)

    def file_path(self, request, response=None, info=None) -> str:
        return f"images/{request.url.split('/')[-1]}"

class ScraperPipeline:
    def process_item(self, item, spider):
        return item
