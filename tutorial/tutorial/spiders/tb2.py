# -*- coding: utf-8 -*-
import scrapy


class Tb2Spider(scrapy.Spider):
    name = "tb2"
    allowed_domains = ["http://s.2.taobao.com/list/list.htm?catid=50100423"]
    start_urls = (
        'http://www.http://s.2.taobao.com/list/list.htm?catid=50100423/',
    )

    def parse(self, response):
        pass
