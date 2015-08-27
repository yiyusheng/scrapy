# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import *

from items import DeiyiItem


# generate urls
urls = 'http://m.deyi.com/forum.php?mod=forumdisplay&type=new&fid=23&mobile=yes&typeid=0&page=' 

class ErshouSpider(scrapy.Spider):
# parameter
    name = "deyi"
    allowed_domains = ["http://m.deyi.com/"]
    start_urls = [urls + `i` for i in range(1,2)]

# parse
    def parse(self, response):	
        item = DeiyiItem()
        datenow = datetime.now() 
        time_emu = ('分钟前','小时前','天前')
        time_minute = time_emu[0].decode('utf-8')
        time_hour = time_emu[1].decode('utf-8')
        time_day = time_emu[2].decode('utf-8')
		
		# parse info from response
        title = response.xpath('//*[@class="text"]/p/text()').extract()
        url = response.xpath('//*[@id="content"]/section/a/@href').extract()
        id_time = response.xpath('//*[@class="name"]/h4/text()').extract()
        comments = response.xpath('//*[@class="name"]/span/text()').extract()
		
		# fill info into item
        for i in range(len(title)):
            item['title'] = title[i]
            item['url'] = url[i]
            tmp = id_time[i].split(' / ')
            item['id'] = tmp[0]
            time = tmp[1]
            if time_minute in time:
                tmp = time.replace(time_minute,'')
                delta = timedelta(minutes = int(tmp))
                item['time'] = datenow - delta
            elif time_hour in time:
                tmp = time.replace(time_hour,'')
                delta = timedelta(hours = int(tmp))
                item['time'] = datenow - delta
            elif time_day in time:
                tmp = time.replace(time_day,'')
                delta = timedelta(days = int(tmp))
                item['time'] = datenow - delta
            else:
                item['time'] = time
            item['comments'] = comments[i]
            yield item
		