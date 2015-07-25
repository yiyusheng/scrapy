# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQL_Class as mc
import re
import csv

# MySQL config
host = 'localhost'
user = 'root'
passwd = 'qwer1234'

# DB info
DB = 'scrapy'
Table = 'ershoujie'


# Pipeline
class ErshoujieMySQLPipeline(object):
    def __init__(self):
# Connect to db
        self.ms = mc.MC(host,user,passwd)
        self.ms.connectDB()
        self.ms.selectDB(DB)

    def process_item(self, item, spider):
        sqlstr = '''INSERT IGNORE INTO %s (good_id,title,price,descr,time,id,city,comment_count,favorite_count,url,img_url,class) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' %(Table,item['good_id'],item['title'],item['price'],item['desc'],item['time'],item['wangwang'],item['city'],item['comment_count'],item['favorite_count'],item['url'],item['image_url'],item['cls'])
        r = self.ms.executeDB(sqlstr)
        return item
