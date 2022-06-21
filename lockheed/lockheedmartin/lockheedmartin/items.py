# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, TakeFirst


class DocumentItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    image_urls = scrapy.Field()
    image = scrapy.Field()
    youtube_urls = scrapy.Field()