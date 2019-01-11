# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class DeyiwebSpider(CrawlSpider):
    name = 'deyi'
    allowed_domains = ['deyi.com']

    def start_requests(self):
        urls = ['http://www.deyi.com/forum-forumdisplay-fid-23-filter-author-orderby-dateline-page-' + str(i) + '.html' for i in range(1,3)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)

        
        for it in rx:
           replyTime = it.xpath('tr/td[4]/em/a/text()').extract()[0]
           replyCount = it.xpath('tr/td[3]/a/text()').extract()
           if len(replyCount)==0:
               continue
           else:
               replyCount=replyCount[0]
           if int(replyCount)==0:
               finalTime = datetime.strptime(replyTime+':00','%Y-%m-%d %H:%M:%S')
               finalTime = finalTime+timedelta(hours=-8)
           else:
               finalTime = utcTime
           #finalTime = int(replyCount)==0 and replyTime+':00' or e8Time
           
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a[1]/text()').extract()[0]
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://www.deyi.com/forum-viewthread-tid-')+'.html'
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
#//*[@id="normalthread_11040653"]/tr/td[4]/em/a
