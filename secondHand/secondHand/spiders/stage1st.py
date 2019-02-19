# -*- coding: utf-8 -*-
import scrapy,os,json
from datetime import datetime,timedelta
from scrapy.spiders import CrawlSpider
from secondHand.items import SecondhandItem
from scrapy.conf import settings
from scrapy.http import FormRequest


class Stage1stSpider(CrawlSpider):
    name = 'stage1st'
    allowed_domains = ['saraba1st.com']
    cookie = settings['COOKIE_stage1st']
    urls = ['https://bbs.saraba1st.com/2b/forum.php?mod=forumdisplay&fid=115&orderby=dateline&filter=author&orderby=dateline&page=' + str(i) for i in range(1,2)]
    start_url = urls[0]

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.login)
            
    def login(self,response):
        #path_config = os.path.expanduser('~')+'/Data/secondHand/'+self.name
        path_config = '/home/yiyusheng/Data/secondHand/'+self.name
        data_config = json.load(open(path_config))
        return [FormRequest.from_response(response,formdata=data_config,callback=self.check_login_usable)]
    
    def check_login(self,response):
        if "登陆失败" in response.body:
            self.log("Login failed.")
        else:
            self.log("Successfully logged in. Start crawling...")
            for url in self.urls:
                yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self,response):
        rx = response.xpath("//tbody[contains(@id,'normalthread')]")
        utcTime = datetime.utcnow().replace(second=0,microsecond=0)
        for it in rx:
           item = SecondhandItem()
           item['title'] = it.xpath('tr/th/a/text()').extract()
           item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
           item['time'] = it.xpath('tr/td[2]/em/span/text()').extract()
           item['time'] = datetime.strptime(item['time'][0],'%Y-%m-%d %H:%M')+timedelta(hours=-8) 
           item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
           item['create_time'] = utcTime
           item['webname'] = self.name
           item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','https://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=')
           
           item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
           item['price'] = ''
           item['location'] = ''
           item['ext4'] = ''
           item['ext5'] = ''
           yield item    
           
           
    def check_login_usable(self,response):
        if "登陆失败" in response.body:
            self.log("Login failed.")
        else:
            self.log("Successfully logged in. Start crawling...")
            rx = response.xpath("//tbody[contains(@id,'normalthread')]")
            utcTime = datetime.utcnow().replace(second=0,microsecond=0)
            for it in rx:
               item = SecondhandItem()
               item['title'] = it.xpath('tr/th/a/text()').extract()[0]
               item['uname'] = it.xpath('tr/td[2]/cite/a/text()').extract()
               item['time'] = it.xpath('tr/td[2]/em/span/text()').extract()
               item['time'] = datetime.strptime(item['time'][0],'%Y-%m-%d %H:%M')+timedelta(hours=-8) 
               item['reply_count'] = it.xpath('tr/td[3]/a/text()').extract()
               item['create_time'] = utcTime
               item['webname'] = self.name
               item['url'] = it.xpath('@id').extract()[0].replace('normalthread_','https://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=')
               
               item['view_count'] = it.xpath('tr/td[3]/em/text()').extract()
               item['price'] = ''
               item['location'] = ''
               item['ext4'] = ''
               item['ext5'] = ''
               yield item
           
#drop table test;create table test like secondHand;
