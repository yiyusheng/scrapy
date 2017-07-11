# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dgtle.items import DgtleWebItem


class NewsmthwebSpider(CrawlSpider):
    name = 'newsmthWeb'
    allowed_domains = ['newsmth.net']

    def start_requests(self):
        urls = ['http://www.newsmth.net/nForum/#!board/SecondComputer?p=' + str(i) for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id="body"]/div[3]/table/tbody")
        for it in rx:
           item = DgtleWebItem()
           item['uname'] = it.xpath('div[2]/p[2]/text()').extract()
           item['create_time'] = datetime.datetime.now()
           item['time'] = it.xpath('p[2]/span[1]/text()').extract()
           item['reply_count'] = it.xpath('p[2]/span[3]/text()').extract()
           item['title'] = it.xpath('div[2]/p[1]/@title').extract()
           item['location'] = it.xpath('p[1]/font-size/span/text()').extract()
           item['url'] = it.xpath('div[2]/p[1]/a/@href').extract() 
           item['view_count'] = it.xpath('p[2]/span[2]/text()').extract()
           item['price'] = it.xpath('p[1]/font-size/text()').extract()
           yield item
