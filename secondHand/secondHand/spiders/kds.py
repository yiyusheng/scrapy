# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class KDSSpider(CrawlSpider):
    name = 'KDS'
    allowed_domains = ['kdslife.com']

    def start_requests(self):
        urls = ['https://club.kdslife.com/f_35_0_0_'+ str(i) +'.html' for i in range(1,2) ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//li[@class='i2']")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('span[3]/a/text()').extract()[0]
           item['uname'] = it.xpath('span[5]/a/text()').extract()
           item['time'] = it.xpath('span[6]/text()').extract()
           item['time'] = datetime.strptime('20'+item['time'][0],'%Y-%m-%d %H:%M')+timedelta(hours=-8) 
           item['reply_count'] = it.xpath('span[4]/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = 'https://club.kdslife.com/' + it.xpath('span[3]/a/@href').extract()[0]
           
           item['view_count'] = it.xpath('span[2]/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
