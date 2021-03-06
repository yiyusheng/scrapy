# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class SmzdmSpider(CrawlSpider):
    name = 'smzdm'
    allowed_domains = ['2.smzdm.com']

    def start_requests(self):
        urls = ['https://2.smzdm.com/p' + str(i) + '/' for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//li[contains(@class,'second_li')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        e8Time = utcTime + timedelta(hours=8)
        for it in rx:
           rawTime = it.xpath('div[3]/text()').extract()[0]
           
           if rawTime.count('-') == 1:
               finalTime = '2017-'+rawTime + ':00'
           elif rawTime.count('-') == 2:
               finalTime = rawTime + ':00'
           else:
               finalTime = e8Time.strftime('%Y-%m-%d ') + str(rawTime) + ':00'
           finalTime = datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S')
           if finalTime > e8Time:
               finalTime = e8Time
            
           item = SecondhandItem()
           item['title'] = it.xpath('div[9]/a/text()').extract()
           item['uname'] = it.xpath('div[2]/a/text()').extract()
           item['time'] = finalTime+timedelta(hours=-8)
           item['reply_count'] = it.xpath('div[7]/a/em/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('div[9]/a/@href').extract()
           
           item['view_count'] = ''
           item['price'] = it.xpath('div[6]/span/text()').extract()
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
#[it.xpath('tr/td[2]/em/span/font/text()').extract() for it in rx]
