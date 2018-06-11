# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class imp3Spider(CrawlSpider):
    name = 'imp3'
    allowed_domains = ['imp3.net']
    
    def start_requests(self):
        urls = ['http://bbs.imp3.net/forum.php?mod=forumdisplay&fid=63&orderby=dateline&filter=author&orderby=dateline&page=' + str(i)  for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()         
           item['title'] = it.xpath('tr/th/a[3]/text()').extract()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = utcTime
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://bbs.imp3.net/forum.php?mod=viewthread&tid=')
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#//*[@id="normalthread_12221084"]/tr/th/a[3]
#//*[@id="normalthread_12221084"]/tr/td[2]/cite/a
#//*[@id="normalthread_12221084"]/tr/td[2]/em/span
#//*[@id="normalthread_12221084"]/tr/td[3]/a
#http://bbs.imp3.net/forum.php?mod=viewthread&tid=
