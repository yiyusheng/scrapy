# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from datetime import datetime,timedelta
from secondHand.items import SecondhandItem

class DgtleWebSpider(CrawlSpider):
    name = 'dgtle'
    allowed_domains = ['dgtle.com']

    def start_requests(self):
        urls = ['http://www.dgtle.com/sale']
        #urls = ['http://bbs.dgtle.com/dgtle_module.php?mod=trade&ac=index&typeid=&PName=&searchsort=0&page=' + str(i) for i in range(1,6)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        url_prefix = "http://www.dgtle.com"
        rx = response.xpath("//a[contains(@class,'idle-content-list-1')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('div[2]/p/text()').extract()[0]
           uname = it.xpath('div[2]/div[2]/span[2]/text()').extract()[0]
           item['uname'] = uname.split(u'·')[1]
           item['time'] = utcTime
           item['reply_count'] = ''
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = url_prefix+it.xpath('@href').extract()[0]
           item['view_count'] = ''
           item['price'] = it.xpath('div[2]/div[1]/text()').extract()[0]
           item['location'] = it.xpath('div[2]/div[2]/span[1]/text()').extract()[0]
           item['ext4'] = ''
           item['ext5'] = ''
           #print item['title'],item['uname'],item['url'],item['price'],item['location']
           yield item
