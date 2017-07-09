# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeyishenghuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    uname = scrapy.Field()
    time = scrapy.Field()
    difftime = scrapy.Field()	
    reply_count = scrapy.Field()	
    detail = scrapy.Field()	
    url = scrapy.Field()	
