# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(host = settings['MONGODB_HOST'], port = settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DBNAME']]
        self.url_collection = db['url']
        self.shop_collection = db['shop']
        self.comment_collection = db['comment']
        self.user_collection = db['member']

    def update(self, collection, item):
        try:
            collection.insert(dict(item))
            return item
        except:
            raise DropItem('Item already exists.')

    def process_item(self, item, spider):
        if spider.name == 'urlSpider':
            self.update(self.url_collection, item)
        if spider.name == 'shopSpider':
            self.update(self.shop_collection, item)
        if spider.name == 'commentSpider':
            self.update(self.comment_collection, item)
        if spider.name == 'userSpider':
            self.update(self.user_collection, item)

class DazhongdianpingPipeline(object):
    def process_item(self, item, spider):
        return item