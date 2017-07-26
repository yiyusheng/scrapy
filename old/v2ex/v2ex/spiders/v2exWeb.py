# -*- coxing: utf-8 -*-
import scrapy
import datetime
from scrapy.spiders import CrawlSpider
from v2ex.items import v2exItem


class v2exWebSpider(CrawlSpider):
    name = 'v2exWeb'
    allowed_domains = ['v2ex.com']

    def start_requests(self):
        urls = ['https://www.v2ex.com/go/all4all?p=' + str(i) for i in range(1,3)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//*[@id='TopicsNode']")
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        for it in rx:
           item = v2exItem()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['create_time'] = datetime.datetime.utcnow()
           item['time'] = it.xpath('tr/td[2]/em/text()').extract()
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['title'] = it.xpath('tr/th/a[1]/text()').extract()
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://www.deyi.com/forum-viewthread-tid-')+'.html'
           yield item
