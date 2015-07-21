# -*- coding: utf-8 -*-
import scrapy

from item import goodItem


class ErshouSpider(scrapy.Spider):
    name = "ershoujie"
    allowed_domains = ["http://s.2.taobao.com/"]
# generate urls
    ori_urls = 'http://s.2.taobao.com/list/list.htm?catid=50100423&st_edtime=1&page='
    start_urls = [ori_urls + `i` for i in range(1,101)]
#    start_urls = (
#        'http://s.2.taobao.com/list/list.htm?catid=50100423',
#        'http://s.2.taobao.com/list/list.htm?catid=50100423&st_edtime=1&page=6'
#    )

    def parse(self, response):
        item = goodItem()
        title_url = response.xpath('//*[@class="item-info"]')
        price = response.xpath('//*[@class = "item-price price-block"]/span/em/text()').extract()
        description = response.xpath('//*[@class="item-description"]/text()').extract()
        for i in range(len(title_url)):
            item['title'] = title_url.xpath('//h4/a/text()').extract()[i]
            item['url'] = 'http:' + title_url.xpath('//h4/a/@href').extract()[i]
            item['price'] = price[i]
            item['desc'] = description[i]
            yield item
