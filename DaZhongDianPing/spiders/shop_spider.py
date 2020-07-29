# -*- coding: utf-8 -*-

# Created by Saki on 2016/12/21.

import re
import string
import pymongo

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider
from DaZhongDianPing.items import ShopItem

class shopSpider(CrawlSpider):
    name = 'shopSpider'
    redis_key = 'shopSpider:start_urls'
    start_urls = []
    connection = pymongo.MongoClient(host = settings['MONGODB_HOST'], port = settings['MONGODB_PORT'])
    db = connection[settings['MONGODB_DBNAME']]
    all_shops = db['url'].find()
    urls = []
    for each in all_shops:
        urls.append(each['url'])
    connection.close()
    start_urls.append(urls[0])
    cnt = 0

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml', from_encoding = 'utf-8')
        cur_url = soup.find('link', rel = 'canonical')['href']
        cata1 = soup.find('a', class_ = 'current-category J-current-category').get_text().strip()
        bread = soup.find('div', class_ = 'breadcrumb').find_all('a')
        info = soup.find('div', id = 'basic-info')
        tags = soup.find_all('span', class_ = re.compile(r'(good J-summary)|(bad J-summary)'))
        flag = True
        shop_closed = info.find('p', class_ = 'shop-closed')
        if shop_closed is not None:
            flag = False
        shop_id = cur_url.replace('http://www.dianping.com/shop/', '')
        shop_name = info.find('h1', class_ = 'shop-name').stripped_strings.next()
        tels = info.find('span', class_ = 'info-name', text = u'电话：').find_all_next('span', itemprop = 'tel')
        tel = ''
        tel_cnt = 0
        for t in tels:
            tel += str(t.get_text())
            tel_cnt += 1
            if tel_cnt != len(tels):
                tel += ' '
        address = info.find('span', class_ = 'info-name', text = u'地址：').find_next('span', class_ = 'item').get_text().strip()
        open_time = ''
        if flag is True:
            open_time = info.find('p', class_ = 'info info-indent').find('span', class_ = 'info-name')
            if open_time.get_text().strip() != u'营业时间：':
                open_time = open_time.find_next('span', class_ = 'info-name')
            open_time = open_time.find_next('span', class_ = 'item').get_text().strip()
        array = []
        for arr in bread:
            array.append(arr.get_text().strip())
        area = array[1]
        cata2 = ''
        for i in range(2, len(array)):
            if i != 2:
                cata2 += ' '
            cata2 += array[i]
        star = comment = avg = ''
        tag1 = tag2 = tag3 = ''
        spans = info.find('div', class_ = 'brief-info').find_all('span')
        for span in spans:
            if span['class'] != ['item']:
                star = re.compile(r'\d+').search(span['class'][1]).group()
                star = str(string.atof(star) / 10)
            else:
                num = re.compile(r'\-|\d\.\d|\d+').search(span.get_text()).group()
                if span.get_text().find(u'条评论') != -1:
                    comment = num
                if span.get_text().find(u'人均：') != -1:
                    avg = num
                if span.get_text().find(u'口味：') != -1:
                    tag1 = num
                if span.get_text().find(u'环境：') != -1:
                    tag2 = num
                if span.get_text().find(u'服务：') != -1:
                    tag3 = num
        all_tags = ''
        tag_no = 0
        for tag in tags:
            if tag_no != 0:
                all_tags += ' '
            name = tag.a.get_text()
            all_tags += name
            tag_no += 1
        item = ShopItem()
        item['_id'] = shop_id
        item['name'] = shop_name
        item['tel'] = tel
        item['address'] = address
        item['open_time'] = open_time
        item['cata1'] = cata1
        item['cata2'] = cata2
        item['area'] = area
        item['comment'] = comment
        item['avg'] = avg
        item['star'] = star
        item['tag1']= tag1
        item['tag2'] = tag2
        item['tag3'] = tag3
        item['all_tags'] = all_tags
        yield item
        self.cnt += 1
        try:
            yield Request(self.urls[self.cnt], callback = self.parse)
        except:
            pass