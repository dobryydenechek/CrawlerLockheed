# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
# from urlparse import urljoin
from urllib.parse import urljoin
from ..items import DocumentItem
from datetime import datetime


class LockheedSpider(scrapy.Spider):
    name = 'lockheed'
    start_urls = ['https://news.lockheedmartin.com/news-releases']

    def parse(self, response):
        next_page_path = '//*[@class="wd_page_link wd_page_next"]/a/@href'
        news_blocks_path = "//*[@class='wd_item_wrapper']/div[@class='wd_title']/a/@href"
        
        news_urls = response.xpath(news_blocks_path).extract()

        for news_url in news_urls:
            url = urljoin(response.url, news_url)
            yield Request(url, callback=self.parse_item)

        next_page_url = response.xpath(next_page_path).extract_first()

        if next_page_url and news_urls:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_item(self, response):
        item = DocumentItem()
        title_path = "//*[@class='wd_title wd_language_left']/text()"
        text_path = "//*[@class='wd_body wd_news_body']//p//text()"
        
        images_path = "//*[@class='wd_image']/img/@src"

        media_urls_path = "//*/iframe/@src"
        
        media_urls = [iframe for iframe in response.xpath(media_urls_path).extract() if "www.youtube.com" in iframe]
        item['youtube_urls'] = media_urls


        item['url'] = response.request.url

        title = response.xpath(title_path).extract_first()

        if title:
            item['title'] = title.strip()
        else:
            item['title'] = ""
            self.logger.error('Missing title news')

        text_blocks = response.xpath(text_path).extract()
        text_delimiter = self.settings.get('TEXT_DELIMITER')

        if text_blocks:
            item['text'] = text_delimiter.join([text_block.strip() for text_block in text_blocks])
        else:
            item['text'] = ''

        images_urls = [urljoin(response.url, href) for href in response.xpath(images_path).extract()]
        item['image_urls'] = images_urls


        yield item
