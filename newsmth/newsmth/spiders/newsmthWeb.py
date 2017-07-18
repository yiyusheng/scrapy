# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from newsmth.items import NewsmthItem


class NewsmthwebSCSpider(CrawlSpider):
    name = 'newsmthWebSC'
    allowed_domains = ['newsmth.net']

    def start_requests(self):
        urls = ['http://www.newsmth.net/nForum/board/SecondComputer?p=' + str(i) for i in range(1,100)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='body']/div[3]/table/tbody/tr[not(@class)]")
        for it in rx:
           item = NewsmthItem()
           item['uname'] = it.xpath('td[4]/a/text()').extract()
           item['time'] = it.xpath('td[3]/text()').extract()
           item['reply_count'] = it.xpath('td[7]/text()').extract()
           item['title'] = it.xpath('td[2]/a/text()').extract()
           item['url'] = 'http://www.newsmth.net'+it.xpath('td[2]/a/@href').extract()[0]
           item['create_time'] = datetime.datetime.utcnow().replace(second=0,microsecond=0)
           yield item
           
class NewsmthwebSDSpider(CrawlSpider):
    name = 'newsmthWebSD'
    allowed_domains = ['newsmth.net']

    def start_requests(self):
        urls = ['http://www.newsmth.net/nForum/board/SecondDigi?p=' + str(i) for i in range(1,50)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='body']/div[3]/table/tbody/tr[not(@class)]")
        for it in rx:
           item = NewsmthItem()
           item['uname'] = it.xpath('td[4]/a/text()').extract()
           item['time'] = it.xpath('td[3]/text()').extract()
           item['reply_count'] = it.xpath('td[7]/text()').extract()
           item['title'] = it.xpath('td[2]/a/text()').extract()
           item['url'] = 'http://www.newsmth.net'+it.xpath('td[2]/a/@href').extract()[0]
           item['create_time'] = datetime.datetime.utcnow().replace(second=0,microsecond=0)
           yield item
           