# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem

class FengSpider(CrawlSpider):
    name = 'feng'
    allowed_domains = ['bbs.feng.com']

    def start_requests(self):
        urls = ['https://www.feng.com/forum/30?page=' + str(i) for i in range(1,3)]
        #urls = ['http://bbs.feng.com/forum.php?mod=forumdisplay&fid=29&orderby=dateline&filter=author&orderby=dateline&page=' + str(i) for i in range(1,3)]
#        urls = ['http://bbs.feng.com/thread-htm-fid-29-page-' + str(i) + '.html' for i in range(1,101)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//div[contains(@class,'content-box')]")
        utcTime = datetime.utcnow().replace(microsecond=0)
        for it in rx:
           item = SecondhandItem()
           
           item['title'] = it.xpath('div[1]/div[2]/div[1]/a/text()').extract()[0]
           item['uname'] = it.xpath('div[1]/div[2]/div[2]/span[1]/text()').extract()[0]
           item['time'] = utcTime
           item['reply_count'] = it.xpath('div[2]/div/ul/li[2]/span/text()').extract()[0]
           item['create_time'] = utcTime.replace(second=0)
           item['webname'] = self.name
           item['url'] = 'https://www.feng.com' + it.xpath('div[1]/div[2]/div[1]/a/@href').extract()[0]
           
           item['view_count'] = it.xpath('div[2]/div/ul/li[1]/span/text()').extract()[0]
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
