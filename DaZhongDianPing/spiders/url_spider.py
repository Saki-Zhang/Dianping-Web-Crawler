# -*- coding: utf-8 -*-

# Created by Saki on 2016/12/21.

import urlparse

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from DaZhongDianPing.items import UrlItem

class urlSpider(CrawlSpider):
    name = 'urlSpider'
    redis_key = 'urlSpider:start_urls'
    start_urls = ['http://www.dianping.com/search/category/4/10']

    url = 'http://www.dianping.com/search/category/4/10'

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml', from_encoding = 'utf-8')
        shop_list = soup.find('div', class_ = 'shop-list J_shop-list shop-all-list')
        lis = shop_list.find_all('li')
        for li in lis:
            tit = li.find('div', class_ = 'tit')
            name = tit.a.h4.get_text()
            page = tit.a['href']
            item = UrlItem()
            item['_id'] = page.replace('/shop/', '')
            item['name'] = name
            item['url'] = urlparse.urljoin(self.url, page)
            yield item
        next_page = soup.find('a', class_ = 'next')
        if next_page is not None:
            next_url = urlparse.urljoin(self.url, next_page['href'])
            yield Request(next_url, callback = self.parse)