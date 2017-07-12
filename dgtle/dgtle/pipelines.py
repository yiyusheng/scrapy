# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import signals
from scrapy.exporters import CsvItemExporter
import time
import pymysql

#%% save as CSV files
class DgtleWebCSVPipeline(object):
    def __init__(self):
        self.files = {}
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('/home/yiyusheng/Data/scrapy/'+spider.name+'/'+time.strftime('%Y-%m-%d-%H'),'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
    def get_media_requests(self, item, info):
        info.spider.name



#%% save in MySQL
def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "qwer1234",
        charset = "utf8",
        use_unicode = True
    )
    return conn
    
class DgtleWebMySQLPipeline(object):
    def process_item(self,item,spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE scrapy")
        cursor.execute("set names 'utf8';")
        cursor.execute("set character set utf8;")
        sql = "INSERT IGNORE INTO secondHand(title,uname,time,reply_count,create_time,webname,url,ext1,ext2,ext3) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql,(item['title'],item['uname'],item['time'],item['reply_count'],item['create_time'],spider.name,item['url'],
                                item['view_count'],item['price'],item['location']))
            cursor.connection.commit()
        except BaseException as e:
            print("?????>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<?????")
            dbObject.rollback()
        return item