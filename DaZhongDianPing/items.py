# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DazhongdianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UrlItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()

class ShopItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()
    address = scrapy.Field()
    open_time = scrapy.Field()
    cata1 = scrapy.Field()
    cata2 = scrapy.Field()
    area = scrapy.Field()
    comment = scrapy.Field()
    avg = scrapy.Field()
    star = scrapy.Field()
    tag1 = scrapy.Field()
    tag2 = scrapy.Field()
    tag3 = scrapy.Field()
    all_tags = scrapy.Field()

class CommentItem(scrapy.Item):
    _id = scrapy.Field()
    shop_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    rank = scrapy.Field()
    tag1 = scrapy.Field()
    tag2 = scrapy.Field()
    tag3 = scrapy.Field()
    avg = scrapy.Field()
    like = scrapy.Field()

class UserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    is_vip = scrapy.Field()
    contribution = scrapy.Field()
    birth = scrapy.Field()
    city = scrapy.Field()
    gender = scrapy.Field()