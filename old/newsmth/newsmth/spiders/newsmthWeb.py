# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from newsmth.items import NewsmthItem


class NewsmthwebSCSpider(CrawlSpider):
    name = 'newsmthWebSC'
    allowed_domains = ['newsmth.net']

    def start_requests(self):
        urls = ['http://www.newsmth.net/nForum/board/SecondComputer?p=' + str(i) for i in range(1,5)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='body']/div[3]/table/tbody/tr[not(@class)]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)

        for it in rx:
           rawTime = it.xpath('td[3]/text()').extract()[0]
           if u'-' in rawTime:
               finalTime = rawTime + ' 00:00:00'
           elif int(rawTime[0:2]) >= 8:
               finalTime = utcTime.strftime('%Y-%m-%d ') + str(rawTime.replace(u'\u2003',''))
           else:
               finalTime = (utcTime + timedelta(days=1)).strftime('%Y-%m-%d ') + str(rawTime.replace(u'\u2003',''))

            
           item = NewsmthItem()
           item['uname'] = it.xpath('td[4]/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = it.xpath('td[7]/text()').extract()
           item['title'] = it.xpath('td[2]/a/text()').extract()
           item['url'] = 'http://www.newsmth.net'+it.xpath('td[2]/a/@href').extract()[0]
           item['create_time'] = utcTime
           yield item
           
class NewsmthwebSDSpider(CrawlSpider):
    name = 'newsmthWebSD'
    allowed_domains = ['newsmth.net']

    def start_requests(self):
        urls = ['http://www.newsmth.net/nForum/board/SecondDigi?p=' + str(i) for i in range(1,5)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='body']/div[3]/table/tbody/tr[not(@class)]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)

        for it in rx:
           rawTime = it.xpath('td[3]/text()').extract()[0]
           if u'-' in rawTime:
               finalTime = rawTime + ' 00:00:00'
           elif int(rawTime[0:2]) >= 8:
               finalTime = utcTime.strftime('%Y-%m-%d ') + str(rawTime.replace(u'\u2003',''))
           else:
               finalTime = (utcTime + timedelta(days=1)).strftime('%Y-%m-%d ') + str(rawTime.replace(u'\u2003',''))
            
           item = NewsmthItem()
           item['uname'] = it.xpath('td[4]/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = it.xpath('td[7]/text()').extract()
           item['title'] = it.xpath('td[2]/a/text()').extract()
           item['url'] = 'http://www.newsmth.net'+it.xpath('td[2]/a/@href').extract()[0]
           item['create_time'] = utcTime
           yield item
           