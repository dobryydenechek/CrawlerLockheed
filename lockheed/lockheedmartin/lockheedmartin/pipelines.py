# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import hashlib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from scrapy.utils.project import get_project_settings
from pytube import YouTube
import logging
from hashlib import sha1

class LockheedmartinPipeline:
    def process_item(self, item, spider):
        return item
class LockheedmartinImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['image_urls']:
            for img_url in item['image_urls']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as err:
                    print(err)

    def item_completed(self, results, item, info):
        item['image_urls'] = [el[1] for el in results if el[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        sub_dir = item['title'].replace('/', '-')
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{sub_dir}/{image_guid}.jpeg'

class YoutubePipeline(object):
    settings = get_project_settings()
    DOWNLOAD_YOUTUBE = settings.get('DOWNLOAD_YOUTUBE')


    def process_item(self, item, spider):
        if not self.DOWNLOAD_YOUTUBE:
            return item

        youtube_urls = item.get('youtube_urls')

        if not youtube_urls:
            return item

        for media_url in youtube_urls:
            try:
                yt = YouTube(media_url)
                stream = yt.streams.filter(subtype='mp4').filter(progressive=True).first()
            except:
                logging.warning('%s video unavailable' % media_url)
                return item
            filename = media_url.replace('/', '-')
            stream.download('../youtubevids', filename=filename)
            logging.debug('Downloaded youtube video from %s' % media_url)

        return item
