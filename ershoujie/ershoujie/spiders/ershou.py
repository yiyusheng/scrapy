# -*- coding: utf-8 -*-
import scrapy


class ErshouSpider(scrapy.Spider):
    name = "ershou"
    allowed_domains = ["http://s.2.taobao.com/"]
    start_urls = (
        'http://s.2.taobao.com/list/list.htm?catid=50100423/',
    )

    def parse(self, response):
        item = goodItem()
        for sel in response.xpath('//li/div'):
        item['url'] = 
        item['title'] = 
        item['price'] = 

