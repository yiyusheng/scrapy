# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class XitekSpider(CrawlSpider):
    name = 'xitek'
    allowed_domains = ['xitek.com']

    def start_requests(self):
        urls = ['http://forum.xitek.com/forum-forumdisplay-fid-44-filter-author-orderby-tid-page-'+str(i)+'.html' for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a/text()').extract()[0]
           item['uname'] = it.xpath('tr/td[2]/a/text()').extract()[0]
           item['time'] = utcTime
           item['reply_count'] = it.xpath('tr/td[3]/text()').extract()[0]
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = 'http://forum.xitek.com/'+it.xpath('tr/th/a/@href').extract()[0]
           item['view_count'] = it.xpath('tr/td[4]/text()').extract()[0]
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
