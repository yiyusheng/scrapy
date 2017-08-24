# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class it168Spider(CrawlSpider):
    name = 'it168'
    allowed_domains = ['it168.com']

    def start_requests(self):
        urls = ['http://benyouhui.it168.com/forum.php?mod=forumdisplay&fid=271&orderby=dateline&orderby=dateline&filter=author&page=' + str(i)  for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/div[1]/h3/a/text()').extract()[0]
           item['uname'] = it.xpath('tr/th/div[2]/p[1]/a/text()').extract()
           item['time'] = it.xpath('tr/th/div[2]/p[1]/span/text()').extract()[0].replace('.','-')+':00'
           item['reply_count'] = it.xpath('tr/th/div[2]/span/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://benyouhui.it168.com/forum.php?mod=viewthread&tid=')
           item['view_count'] = it.xpath('tr/th/div[1]/span[1]/text()').extract()[0].replace('\r\n','')
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
          
#//*[@id="normalthread_5751387"]/tr/th/div[1]/h3/a
#//*[@id="normalthread_5751387"]/tr/th/div[1]/span[1]
#//*[@id="normalthread_5751387"]/tr/th/div[2]/p[1]/a
#//*[@id="normalthread_5751387"]/tr/th/div[2]/p[1]/span
#//*[@id="normalthread_5751387"]/tr/th/div[2]/span
#http://benyouhui.it168.com/forum.php?mod=viewthread&tid=