import scrapy

class goodItem(scrapy.Item):
#good info
    good_id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    time = scrapy.Field()
    image_url =  scrapy.Field()
    comment_count =  scrapy.Field()
    favorite_count =  scrapy.Field()
    cls = scrapy.Field()
    
#seller info
    wangwang =  scrapy.Field()
    city =  scrapy.Field()
    update_time = scrapy.Field()
