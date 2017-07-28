# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql,warnings,datetime

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
    
class SecondhandPipeline(object):
    numDone = 0
    numDup = 0
    numError = 0
    
    def process_item(self,item,spider):
        warnings.filterwarnings('error', category=pymysql.Warning)
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE scrapy")
        cursor.execute("set names 'utf8';")
        cursor.execute("set character set utf8;")
        sql = "INSERT IGNORE INTO secondHand(title,uname,time,reply_count,create_time,webname,url,ext1,ext2,ext3,ext4,ext5) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql,(item['title'],item['uname'],item['time'],item['reply_count'],item['create_time'],spider.name,item['url'],
                                item['view_count'],item['price'],item['location'],item['ext4'],item['ext5']))
            cursor.connection.commit()
            self.numDone += 1
        except BaseException as e:
            if u'Duplicate entry' in str(e):
                self.numDup += 1
            else:
                print("["+datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"]",e)
                self.numError += 1
#            print("["+datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"]",e,item['title'],item['uname'],item['time'],item['reply_count'],item['create_time'],spider.name,item['url'],
#                                item['view_count'],item['price'],item['location'],item['ext4'],item['ext5'])
            dbObject.rollback()
        return item
    def get_statistic(self,spider):
        return {'numDone':self.numDone,'numDup':self.numDup,
                'numError':self.numError,'spider':spider.name}