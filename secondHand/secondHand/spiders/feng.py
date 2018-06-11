# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem

class FengSpider(CrawlSpider):
    name = 'fengWeb'
    allowed_domains = ['bbs.feng.com']

    def start_requests(self):
        urls = ['http://bbs.feng.com/forum.php?mod=forumdisplay&fid=29&orderby=dateline&filter=author&orderby=dateline&page=' + str(i) for i in range(1,3)]
#        urls = ['http://bbs.feng.com/thread-htm-fid-29-page-' + str(i) + '.html' for i in range(1,101)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(microsecond=0)
        for it in rx:
           item = SecondhandItem()
           
           timeA = ''.join(it.xpath('tr/td[2]/em/span/span/@title').extract())
           timeB = ''.join(it.xpath('tr/td[2]/em/span/span/text()').extract()).replace(u'\xa0','')
           timeC = ''.join(it.xpath('tr/td[2]/em/span/text()').extract())
           
           if len(timeC)>0:
               finalTime = timeC + ' 00:00:00'
               finalTime = datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S')+timedelta(hours=-8)
           elif u'天前' in timeB:
               finalTime = timeA + ' 00:00:00'
               finalTime = datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S')+timedelta(hours=-8)
           elif u'前天' in timeB:
               finalTime = timeA + ' ' + timeB.replace(u'前天','') + ':00'
               finalTime = datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S')+timedelta(hours=-8)
           elif u'昨天' in timeB:
               finalTime = timeA + ' ' + timeB.replace(u'昨天','') + ':00'
               finalTime = datetime.strptime(finalTime,'%Y-%m-%d %H:%M:%S')+timedelta(hours=-8)
           elif u'半小时前' in timeB:
               finalTime = utcTime - timedelta(seconds=1800)
           elif u'小时前' in timeB:
               finalTime = utcTime - timedelta(hours=int(timeB.replace(u'小时前','')))
           elif u'分钟前' in timeB:
               finalTime = utcTime - timedelta(minutes=int(timeB.replace(u'分钟前','')))
           elif u'秒前' in timeB:
               finalTime = utcTime - timedelta(seconds=int(timeB.replace(u'秒前','')))
           
           
           finalTime = str(finalTime)
           item['title'] = it.xpath('tr/th/a[1]/text()').extract()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime.replace(second=0)
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','http://bbs.feng.com/read-htm-tid-')+'.html'
           
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
#drop table test;create table test like secondHand;
