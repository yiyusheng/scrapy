# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from datetime import datetime,timedelta
from secondHand.items import SecondhandItem

class DgtleWebSpider(CrawlSpider):
    name = 'dgtleWeb'
    allowed_domains = ['dgtle.com']

    def start_requests(self):
        urls = ['http://bbs.dgtle.com/dgtle_module.php?mod=trade&ac=index&typeid=&PName=&searchsort=0&page=' + str(i) for i in range(1,6)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        url_prefix = "http://bbs.dgtle.com"
        rx = response.xpath("//div[contains(@class,'tradebox')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('div[2]/p[1]/@title').extract()
           item['uname'] = it.xpath('div[2]/p[2]/text()').extract()
           item['time'] = utcTime
           item['reply_count'] = re.findall(r'\d+',it.xpath('p[2]/span[3]/text()').extract()[0])[0]
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = url_prefix+it.xpath('div[2]/p[1]/a/@href').extract()[0]
           item['view_count'] = re.findall(r'\d+',it.xpath('p[2]/span[2]/text()').extract()[0])[0]
           item['price'] = re.findall(r'\d+',it.xpath('p[1]/font-size/text()').extract()[0])[0]
           item['location'] = it.xpath('p[1]/font-size/span/text()').extract()
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
