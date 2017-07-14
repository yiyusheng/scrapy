# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from deyi.items import DeyiWebItem


class DeyiwebSpider(CrawlSpider):
    name = 'deyiWeb'
    allowed_domains = ['deyi.com']

    def start_requests(self):
        urls = ['http://www.deyi.com/forum-forumdisplay-fid-23-filter-author-orderby-dateline-page-' + str(i) + '.html' for i in range(1,3)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        for it in rx:
           item = DeyiWebItem()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['create_time'] = datetime.datetime.utcnow()
           item['time'] = it.xpath('tr/td[2]/em/text()').extract()
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['title'] = it.xpath('tr/th/a[1]/text()').extract()
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://www.deyi.com/forum-viewthread-tid-')+'.html'
           yield item
