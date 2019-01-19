# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class DuowanSpider(CrawlSpider):
    name = 'duowan'
    allowed_domains = ['duowan.com']

    def start_requests(self):
        urls = ['http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=2720&orderby=dateline&orderby=dateline&filter=author&page=1',
                'http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=2355&orderby=dateline&filter=author&orderby=dateline&page=1',
                'http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=1353&orderby=dateline&filter=author&orderby=dateline&page=1']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/span/a/text()').extract()[0]
           item['uname'] = it.xpath('tr/td[2]/cite/a[1]/text()').extract()
           item['time'] = utcTime
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://bbs.duowan.com/forum.php?mod=viewthread&tid=')
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
