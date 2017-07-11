# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from deyi.items import DeyiMobiItem


class DeyimobiSpider(CrawlSpider):
    name = 'deyiMobi'
    allowed_domains = ['m.deyi.com']

    def start_requests(self):
        urls = ['http://m.deyi.com/forum-forumdisplay-fid-23-filter-author-orderby-dateline-typeid-0-page-' + str(i) + '.html' for i in range(1,6)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath('//*[@id="topic"]/section[2]/section/a')
        for it in rx[0:-1]:
           item = DeyiMobiItem()
           item['uname'] = it.xpath('div[1]/div[1]/span/text()').extract()
           item['time'] = datetime.datetime.now()
           item['difftime'] = it.xpath('div[1]/div[2]/time/text()').extract()
           item['reply_count'] = it.xpath('div[1]/div[2]/span/text()').extract()
           item['title'] = it.xpath('div[2]/div[1]/h2/text()').extract()
           item['detail'] = it.xpath('div[2]/div[1]/p/text()').extract()
           item['url'] = it.xpath('@href').extract()    
           yield item