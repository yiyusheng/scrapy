# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem
import re

class v2exSpider(CrawlSpider):
    name = "v2ex"
    allowed_domains = ["v2ex.com"]
    def start_requests(self):
        urls = ['https://www.v2ex.com/?tab=deals']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        rx = response.xpath("//div[contains(@class,'cell item')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('table/tr/td[3]/span[1]/a/text()').extract()[0]
           item['uname'] = it.xpath('table/tr/td[3]/span[2]/strong[1]/a/text()').extract()
           item['time'] = utcTime + timedelta(hours=8)
           item['reply_count'] = it.xpath('table/tr/td[4]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = "https://www.v2ex.com"+re.sub(r"#.*","",it.xpath('table/tr/td[3]/span[1]/a/@href').extract()[0])
           item['view_count'] = ''
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item

