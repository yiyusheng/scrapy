# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from datetime import datetime,timedelta
from secondHand.items import SecondhandItem
import time
from selenium import webdriver


class CHHSpider(CrawlSpider):
    name = 'CHH'
    allowed_domains = ['chiphell.com']

    def start_requests(self):
        urls = ['https://www.chiphell.com/forum.php?mod=forumdisplay&fid=53&orderby=dateline&filter=author&page=' + str(i) for i in range(1,2)]
        #urls = ['https://www.chiphell.com/forum.php?mod=forumdisplay&fid=26&orderby=dateline&filter=author&orderby=dateline&page=' + str(i) for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    
    def parse(self,response):
        url_prefix = "https://www.chiphell.com/"
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a[3]/text()').extract()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = it.xpath('tr/td[2]/em/span/text()').extract()
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = url_prefix+it.xpath('tr/th/a[3]/@href').extract()[0]
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
