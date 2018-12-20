# -*- coding: utf-8 -*-
import scrapy,re
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class B51nbSpider(CrawlSpider):
    name = '51NB'
    allowed_domains = ['51nb.com']

    def start_requests(self):
        urls = ['https://forum.51nb.com/forum.php?mod=forumdisplay&fid=41&filter=author&orderby=dateline']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='moderate']/table/tr/td[2]/table/tr")
        rx = rx[7:]
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('td[1]/a/text()').extract()
           item['uname'] = it.xpath('td[3]/a/text()').extract()
           item['time'] = utcTime
           item['reply_count'] = ''
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = 'https://forum.51nb.com/' + re.sub(r'&extra.*$','',it.xpath('td[1]/a/@href').extract()[0])
           
           item['view_count'] = ''
           item['price'] = it.xpath('td[2]/text()').extract()
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
