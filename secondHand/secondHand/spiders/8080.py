# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class B8080Spider(CrawlSpider):
    name = '8080'
    allowed_domains = ['8080.net']

    def start_requests(self):
        urls = ['http://bbs.8080.net/forum.php?mod=forumdisplay&fid=120&orderby=dateline&filter=author&orderby=dateline&page=' + str(i) for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a[1]/text()').extract()
           item['uname'] = it.xpath('tr/td[2]/cite/text()').extract()[1]
           item['time'] = it.xpath('tr/td[2]/em/span/text()').extract()
           item['time'] = datetime.strptime(item['time'][0],'%Y-%m-%d %H:%M')+timedelta(hours=-8) 
           item['reply_count'] = it.xpath('tr/td[3]/span/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://bbs.8080.net/forum.php?mod=viewthread&tid=')
           
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
