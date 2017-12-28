# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
from datetime import datetime,timedelta
from secondHand.items import SecondhandItem
import time

class NgaSpider(CrawlSpider):
    name = 'nga'
    allowed_domains = ['bbs.nga.cn']

    def start_requests(self):
        urls = ['http://bbs.nga.cn/thread.php?fid=498&order_by=postdatedesc&page=' + str(i) for i in range(1,5)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        url_prefix = "http://bbs.nga.cn"
        rx = response.xpath("//tr[contains(@class,'topicrow')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = re.sub('\[.*\]','',it.xpath('td[2]/a/text()').extract()[0])
           item['uname'] = it.xpath('td[3]/a/@title').extract()
           item['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(it.xpath('td[3]/span/text()').extract()[0])))
           item['reply_count'] = it.xpath('td[1]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = url_prefix+it.xpath('td[1]/a/@href').extract()[0]
           item['view_count'] = ''
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
