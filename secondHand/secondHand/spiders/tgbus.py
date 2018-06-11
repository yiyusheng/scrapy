# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class TgbusSpider(CrawlSpider):
    name = 'tgbusWeb'
    allowed_domains = ['bbs.tgbus.com']

    def start_requests(self):
        urls = ['http://bbs.tgbus.com/forum.php?mod=forumdisplay&fid=50&orderby=dateline&orderby=dateline&filter=author&page=' + str(i) for i in range(1,3)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a[2]/text()').extract()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = it.xpath('tr/td[2]/em/span/text()').extract()
           item['time'] = datetime.strptime(item['time'],'%Y-%m-%d %H:%M:%S')+timedelta(hours=-8) 
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://bbs.tgbus.com/thread-')+'-1-1.html'
           
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
