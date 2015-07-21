import scrapy

class goodItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
