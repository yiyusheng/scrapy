# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql,warnings,datetime,re
from datetime import timedelta

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

def checkempty(item):
    for k in item.keys():
        if item[k]==[]:
            if k in {'view_count','reply_count'}:
                item[k] = 0
            else:
                item[k] = ''
    return(item)
    
class SecondhandPipeline(object):
    numDone = 0
    numDup = 0
    numError = 0
    refresh_webname=['smzdm']
    
    def process_item(self,item,spider):
        warnings.filterwarnings('error', category=pymysql.Warning)
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE scrapy")
        cursor.execute("set names 'utf8';")
        cursor.execute("set character set utf8;")
        try:
            item = checkempty(item)
            sql = "INSERT IGNORE INTO secondHand(title,uname,time,reply_count,create_time,webname,url,ext1,ext2,ext3,ext4,ext5,update_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(item['title'],item['uname'],item['time'],item['reply_count'],item['create_time'],spider.name,item['url'],item['view_count'],item['price'],item['location'],item['ext4'],item['ext5'],item['time']))
            cursor.connection.commit()
            self.numDone += 1

        except BaseException as e:
            if u'Duplicate entry' in str(e):
                if item['webname'] in self.refresh_webname:
                    sql = 'SELECT update_time from secondHand where url=%s and title=%s'
                    cursor.execute(sql,(item['url'],item['title']))
                    uptime_insql = cursor.fetchall()[0][0].strftime('%Y-%m-%d %H:%M:%S')
                    if uptime_insql!=item['time']:
                        #print uptime_insql,item['time'],uptime_insql==item['time']
                        sql = "UPDATE secondHand set update_time=%s,update_count=update_count+1 where url=%s and title=%s"
                        cursor.execute(sql,(item['time'],item['url'],item['title']))
                        cursor.connection.commit()
                self.numDup += 1
            elif u'Incorrect string value' in str(e):
                pass
            else:
                print("["+datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"]\t"+str(e))
                print(item)
                self.numError += 1
            dbObject.rollback()
        return item

    def get_statistic(self,spider):
        return {'numDone':self.numDone,'numDup':self.numDup,
                'numError':self.numError,'spider':spider.name}
