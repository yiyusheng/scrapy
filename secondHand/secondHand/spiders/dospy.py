# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem


class dospySpider(CrawlSpider):
    name = 'dospy'
    allowed_domains = ['dospy.com']

    def start_requests(self):
        urls = ['http://bbs.dospy.com/forumdisplay.php?fid=141&orderby=dateline&page=' + str(i)  for i in range(1,2)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        rx = response.xpath("//table[contains(@class,'word txt_666')]/tr")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)

        for it in rx:
           replyTime = it.xpath('td[4]/u/text()').extract()
           replyCount = it.xpath('td[3]/a/text()').extract()
           if len(replyCount)==0:
               continue
           else:
               replyCount=replyCount[0]
           if int(replyCount)==0:
               finalTime = datetime.strptime(replyTime[0]+':00','%Y-%m-%d %H:%M:%S')
               finalTime = finalTime + timedelta(hours=-8)
           else:
               finalTime = utcTime

            
           item = SecondhandItem()
           item['title'] = it.xpath('th/a/text()').extract()
           item['uname'] = it.xpath('td[2]/cite/a/text()').extract()
           item['time'] = finalTime
           item['reply_count'] = replyCount
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = 'http://bbs.dospy.com/'+it.xpath('th/a/@href').extract()[0]
           
           item['view_count'] = it.xpath('td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item
           
