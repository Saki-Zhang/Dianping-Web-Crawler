# -*- coding: utf-8 -*-

# Created by Saki on 2016/12/21.

import pymongo

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider
from DaZhongDianPing.items import UserItem

class userSpider(CrawlSpider):
    name = 'userSpider'
    redis_key = 'userSpider:start_urls'
    start_urls = []
    connection = pymongo.MongoClient(host = settings['MONGODB_HOST'], port = settings['MONGODB_PORT'])
    db = connection[settings['MONGODB_DBNAME']]
    existed_users = db['member'].find()
    existed_ids = set()
    for each in existed_users:
        existed_ids.add(each['_id'])
    all_comms = db['comment'].find()
    urls = set()
    for each in all_comms:
        if each['user_id'] not in existed_ids:
            urls.add('http://www.dianping.com/member/' + each['user_id'])
    urls = list(urls)
    connection.close()
    start_urls.append(urls[0])
    cnt = 0

    print 'user_cnt =', len(urls)

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml', from_encoding = 'utf-8')
        user_info = soup.find('div', class_ = 'pic-txt head-user')
        user_id = user_info.find('div', class_ = 'pic').a['href'].replace('/member/', '')
        user_name = user_info.find('div', class_ = 'tit').h2.get_text()
        is_vip = user_info.find('div', class_ = 'vip').find('a')
        if is_vip is not None:
            is_vip = '1'
        else:
            is_vip = '0'
        detail = soup.find('div', class_ = 'con')
        try:
            contribution = detail.find('div', class_ = 'user-time').find('p').find('span', id = 'J_col_exp').get_text()
        except:
            contribution = ''
        try:
            birth = ''
            lis = detail.find('div', class_ = 'user-message').find('ul').find_all('li')
            for li in lis:
                if li.get_text().find(u'生日：') != -1:
                    birth = li.get_text()[3:]
                    break
        except:
            birth = ''
        try:
            city = user_info.find('span', class_ = 'user-groun').get_text()
        except:
            city = ''
        try:
            gender = user_info.find('span', class_ = 'user-groun').i['class'][0]
        except:
            gender = ''
        item = UserItem()
        item['_id'] = user_id
        item['name'] = user_name
        item['is_vip'] = is_vip
        item['contribution'] = contribution
        item['birth'] = birth
        item['city'] = city
        item['gender'] = gender
        yield item
        self.cnt += 1
        try:
            yield Request(self.urls[self.cnt], callback = self.parse)
        except:
            pass