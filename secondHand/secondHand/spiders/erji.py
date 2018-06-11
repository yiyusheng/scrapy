# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class erjiSpider(CrawlSpider):
    name = 'erji'
    allowed_domains = ['erji.net']

    def start_requests(self):
        urls = ['http://www.erji.net/forum.php?mod=forumdisplay&fid=8&orderby=dateline&orderby=dateline&filter=author&page=' + str(i)  for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a[2]/text()').extract()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = it.xpath('tr/td[2]/em/span/text()').extract()[0]+':00'
           item['time'] = datetime.strptime(item['time'],'%Y-%m-%d %H:%M:%S')+timedelta(hours=-8)
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://www.erji.net/forum.php?mod=viewthread&tid=')
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
