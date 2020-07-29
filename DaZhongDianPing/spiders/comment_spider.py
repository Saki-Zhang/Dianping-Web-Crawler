# -*- coding: utf-8 -*-

# Created by Saki on 2016/12/21.

import re
import string
import pymongo
import urlparse

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider
from DaZhongDianPing.items import CommentItem

class commentSpider(CrawlSpider):
    name = 'commentSpider'
    redis_key = 'commentSpider:start_urls'
    start_urls = []

    connection = pymongo.MongoClient(host = settings['MONGODB_HOST'], port = settings['MONGODB_PORT'])
    db = connection[settings['MONGODB_DBNAME']]
    existed_shops = db['comment'].find()
    existed_ids = set()
    for each in existed_shops:
        existed_ids.add(each['shop_id'])
    all_shops = db['url'].find()
    urls = []
    for each in all_shops:
        if each['_id'] not in existed_ids:
            urls.append(each['url'] + '/review_more')
    connection.close()
    start_urls.append(urls[0])
    cnt = 0

    print 'shop_cnt =', len(urls)

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml', from_encoding = 'utf-8')
        shop_info = soup.body.find('script', type = 'text/javascript').get_text()
        shop_id = re.search('shopID:(.*?),', shop_info).group(1).replace(' ', '')
        comms = soup.find('div', class_ = 'comment-list')
        comms = comms.find_all('li')
        for comm in comms:
            user_info = comm.find('div', class_ = 'pic')
            if user_info is None:
                continue
            comm_id = comm['data-id']
            user_id = user_info.find('a')['user-id']
            user_name = user_info.find('p', class_ = 'name').get_text()
            detail = comm.find('div', class_ = 'content')
            rank = detail.find('span', class_ = re.compile(r'item-rank-rst irr-star\d\d'))
            if rank is not None:
                rank = str(string.atof(rank['class'][1].replace('irr-star', '')) / 10)
            else:
                rank = ''
            tags = detail.find_all('span', class_ = 'rst')
            array = []
            for tag in tags:
                arr = re.search(r'\d', tag.get_text()).group()
                array.append(arr)
            if len(array) == 3:
                tag1 = array[0]
                tag2 = array[1]
                tag3 = array[2]
            else:
                tag1 = tag2 = tag3 = ''
            avg = detail.find('span', class_ = 'comm-per')
            if avg is not None:
                avg = re.search(r'\d+', avg.get_text()).group()
            else:
                avg = ''
            like = ''
            recmds = detail.find('div', class_ = 'comment-recommend')
            while recmds is not None:
                if recmds.get_text().find(u'喜欢的菜：') == -1:
                    recmds = recmds.find_next('div', class_ = 'comment-recommend')
                    continue
                recmds = recmds.find_all('a')
                recmd_cnt = 0
                for recmd in recmds:
                    if recmd_cnt != 0:
                        like += ' '
                    like += recmd.get_text()
                    recmd_cnt += 1
                break
            item = CommentItem()
            item['_id'] = comm_id
            item['shop_id'] = shop_id
            item['user_id'] = user_id
            item['user_name'] = user_name
            item['rank'] = rank
            item['tag1'] = tag1
            item['tag2'] = tag2
            item['tag3'] = tag3
            item['avg'] = avg
            item['like'] = like
            yield item
            next_page = soup.find('a', class_ = 'NextPage')
            if next_page is not None:
                next_url = urlparse.urljoin(self.urls[self.cnt], next_page['href'])
                yield Request(next_url, callback = self.parse)
            else:
                self.cnt += 1
                try:
                    yield Request(self.urls[self.cnt], callback = self.parse)
                except:
                    pass