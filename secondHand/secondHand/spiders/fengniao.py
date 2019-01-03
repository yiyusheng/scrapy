# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class FengniaoSpider(CrawlSpider):
    name = 'fengniao'
    allowed_domains = ['fengniao.com']

    def start_requests(self):
        urls = ['http://2.fengniao.com/price/add-1_'+ str(i) +'.html' for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//li[@class='goods-item clearfix']")
        rx = rx[:9]+rx[11:]
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('div[2]/a/text()').extract()
           item['uname'] = 'id_'+it.xpath('div[2]/div/div/@data-id').extract()[0]
           item['time'] = utcTime
           item['reply_count'] = ''
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = 'http://2.fengniao.com'+it.xpath('div[2]/a/@href').extract()[0]
           
           item['view_count'] = ''
           item['price'] = it.xpath('div[4]/div/span/em[2]/text()').extract()
           item['location'] = it.xpath('div[2]/div[2]/span/text()').extract()
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
