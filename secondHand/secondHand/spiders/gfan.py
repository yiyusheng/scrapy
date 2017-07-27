# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class GfanSpider(CrawlSpider):
    name = 'gfanWeb'
    allowed_domains = ['bbs.gfan.com']

    def start_requests(self):
        urls = ['http://bbs.gfan.com/forum.php?mod=forumdisplay&fid=23&orderby=dateline&orderby=dateline&filter=author&page=' + str(i) for i in range(1,3)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           timeA = it.xpath('tr/td[2]/em/span/font/text()').extract()
           timeB = it.xpath('tr/td[2]/em/span/text()').extract()
           finalTime = len(timeA)>len(timeB) and timeA or timeB
           
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a/text()').extract()[0]
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://bbs.gfan.com/android-')+'-1-1.html'
           
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
