# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecondhandItem(scrapy.Item):
    title = scrapy.Field()
    uname = scrapy.Field()
    time = scrapy.Field()
    reply_count = scrapy.Field()	
    create_time = scrapy.Field()	
    webname = scrapy.Field()
    url = scrapy.Field()
    
    view_count = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    ext4 = scrapy.Field()
    ext5 = scrapy.Field()
