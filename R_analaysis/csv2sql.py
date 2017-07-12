#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 22:53:59 2017

@author: yiyusheng
"""

import pymysql
import csv

def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "qwer1234",
        charset = "utf8",
        use_unicode = True
    )
    return conn

csv_data = csv.reader(file('/home/yiyusheng/Data/scrapy/dgtleWebAll'))    
    
    
dbObject = dbHandle()
cursor = dbObject.cursor()
cursor.execute("USE scrapy")
cursor.execute("set names 'utf8';")
cursor.execute("set character set utf8;")


a = csv_data.next()
for row in csv_data:
    try:
        #dgtleWeb
        sql = "INSERT IGNORE INTO secondHand(title,uname,time,reply_count,create_time,webname,url,ext1,ext2,ext3) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(row[1],row[4],row[8],row[5],row[6],'dgtleWeb',row[2],row[0],row[3],row[7]))
 
       #deyiWeb
#        sql = "INSERT INTO secondHand(title,uname,time,reply_count,create_time,webname,url,ext1) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
#        cursor.execute(sql,(row[1],row[3],row[6],row[4],row[5],'deyiWeb',row[2],row[0]))

        cursor.connection.commit()
    except BaseException as e:
        print("?????>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<?????")
        dbObject.rollback()
