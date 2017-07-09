#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 09:51:35 2017

@author: yiyusheng
"""

import scrapy
import datetime
from deyishenghuo.items import DeyishenghuoItem

class deyishenghuoSpider(scrapy.Spider):
    name = 'deyishenghuo'
    
    def start_requests(self):
        urls = ['http://m.deyi.com/forum-forumdisplay-fid-23-filter-author-orderby-dateline-typeid-0-page-' + str(i) + '.html' for i in range(1,2)]
#        urls = ['http://www.deyi.com/forum-forumdisplay-fid-23-filter-author-orderby-dateline-page-' + str(i) + '.html' for i in range(1,6)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
#        uname = response.xpath('//*[@id="topic"]/section[2]/section/a/div[1]/div[1]/span').extract()
#        time = response.xpath('//*[@id="topic"]/section[2]/section/a/div[1]/div[2]/time').extract()
#        reply_count = response.xpath('//*[@id="topic"]/section[2]/section/a/div[1]/div[2]/span').extract()
#        title = response.xpath('//*[@id="topic"]/section[2]/section/a/div[2]/div[1]/h2').extract()
#        detail = response.xpath('//*[@id="topic"]/section[2]/section/a/div[2]/div[1]/p').extract()
#        url = response.xpath('//*[@id="topic"]/section[2]/section/a').extract()
        

        
        for item in response.xpath('//*[@id="topic"]/section[2]'):
           item = DeyishenghuoItem()
           
           item['uname'] = item.xpath('section/a/div[1]/div[1]/span').extract()
           item['time'] = datetime.datetime.now()
           item['difftime'] = item.xpath('section/a/div[1]/div[2]/time').extract()
           item['reply_count'] = item.xpath('section/a/div[1]/div[2]/span').extract()
           item['title'] = item.xpath('section/a/div[2]/div[1]/h2').extract()
           item['detail'] = item.xpath('section/a/div[2]/div[1]/p').extract()
           item['url'] = item.xpath('section/a/@href').extract()            
           
           yield item