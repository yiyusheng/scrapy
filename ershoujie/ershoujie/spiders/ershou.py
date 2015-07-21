# -*- coding: utf-8 -*-
import scrapy
from datetime import *

from item import goodItem


class ErshouSpider(scrapy.Spider):
# parameter
    name = "ershoujie"
    allowed_domains = ["http://s.2.taobao.com/"]

# generate urls
    ori_urls = 'http://s.2.taobao.com/list/list.htm?catid=50100423&st_edtime=1&page='
    start_urls = [ori_urls + `i` for i in range(1,101)]

# parse
    def parse(self, response):
        item = goodItem()
        datenow = datetime.now() 
        time_emu = ('分钟前','小时前','天前')
        time_minute = time_emu[0].decode('utf-8')
        time_hour = time_emu[1].decode('utf-8')
        time_day = time_emu[2].decode('utf-8')

# parse info from response
        title_url = response.xpath('//*[@class="item-info"]')
        price = response.xpath('//*[@class = "item-price price-block"]/span/em/text()').extract()
        description = response.xpath('//*[@class="item-description"]/text()').extract()
        time = response.xpath('//*[@class="item-pub-time"]/text()').extract()
        image_url = response.xpath('//*[@class="item-pic sh-pic120"]/a/img/@src').extract() 
        comment_count = response.xpath('//*[@class="item-count"]/a[@class="item-comments"]/em/text()').extract()
        favorite_count = response.xpath('//*[@class="item-count"]/a[@class="item-favorites"]/em/text()').extract()
        wangwang = response.xpath('//*[@class="seller-nick"]/span/@data-nick').extract()
        city = response.xpath('//*[@class="seller-location"]/text()').extract()

# fill info into item
        for i in range(len(title_url)):
            item['title'] = title_url.xpath('//h4/a/text()').extract()[i]
            item['url'] = 'http:' + title_url.xpath('//h4/a/@href').extract()[i]
            item['price'] = price[i]
            item['desc'] = description[i]
            if time_minute in time[i]:
                tmp = time[i].replace(time_minute,'')
                delta = timedelta(minutes = int(tmp))
                item['time'] = datenow - delta
            elif time_hour in time[i]:
                tmp = time[i].replace(time_hour,'')
                delta = timedelta(hours = int(tmp))
                item['time'] = datenow - delta
            elif time_day in time[i]:
                tmp = time[i].replace(time_day,'')
                delta = timedelta(days = int(tmp))
                item['time'] = datenow - delta
            else:
                item['time'] = datetime.strptime(time[i],'%Y.%m.%d')
            item['image_url'] = image_url[i] 
            item['comment_count'] = comment_count[i] 
            item['favorite_count'] = favorite_count[i] 
            item['wangwang'] = wangwang[i] 
            item['city'] = city[i] 
            yield item
