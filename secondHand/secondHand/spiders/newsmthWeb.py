# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem

class NewsmthwebSCSpider(CrawlSpider):
    name = 'smthSC'
    allowed_domains = ['newsmth.net']

    def start_requests(self):
        urls = ['http://www.newsmth.net/nForum/board/SecondComputer?p=' + str(i) for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='body']/div[3]/table/tbody/tr[not(@class)]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        e8Time = utcTime + timedelta(hours=8)
        for it in rx:
           rawTime = it.xpath('td[3]/text()').extract()[0]
           
           if u'-' in rawTime:
               finalTime = rawTime + ' 00:00:00'
           else:
               finalTime = e8Time.strftime('%Y-%m-%d ') + str(rawTime.replace(u'\u2003',''))
           finalTime = datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S')
           #if datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S') > e8Time:
           #    finalTime = e8Time
           
           finalTime = finalTime+timedelta(hours=-8)
           
           item = SecondhandItem()
           item['title'] = it.xpath('td[2]/a/text()').extract()
           item['uname'] = it.xpath('td[4]/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = it.xpath('td[7]/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = 'http://www.newsmth.net'+it.xpath('td[2]/a/@href').extract()[0]
           item['view_count'] = ''
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''

           yield item
           
class NewsmthwebSDSpider(CrawlSpider):
    name = 'smthSD'
    allowed_domains = ['newsmth.net']

    def start_requests(self):
        urls = ['http://www.newsmth.net/nForum/board/SecondDigi?p=' + str(i) for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='body']/div[3]/table/tbody/tr[not(@class)]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        e8Time = utcTime + timedelta(hours=8)
        for it in rx:
           rawTime = it.xpath('td[3]/text()').extract()[0]
           
           if u'-' in rawTime:
               finalTime = rawTime + ' 00:00:00'
           else:
               finalTime = e8Time.strftime('%Y-%m-%d ') + str(rawTime.replace(u'\u2003',''))
           finalTime = datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S')
           #if datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S') > e8Time:
           #    finalTime = e8Time
           finalTime = finalTime+timedelta(hours=-8)
            
           item = SecondhandItem()
           item['title'] = it.xpath('td[2]/a/text()').extract()
           item['uname'] = it.xpath('td[4]/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = it.xpath('td[7]/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = 'http://www.newsmth.net'+it.xpath('td[2]/a/@href').extract()[0]
           item['view_count'] = ''
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
