#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 22:58:14 2017

To extract sellers submit too many items on each site, which occupy much display space of other sellers

@author: yiyusheng
"""

import pymysql,warnings
import pandas as pd
from datetime import datetime,timedelta
from pandas import DataFrame
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

#%% Seller_extract
def advertiser_extract():
    try:
        sql = "SELECT uname,webname,count(*) FROM secondHand WHERE update_time>%s GROUP BY uname,webname HAVING count(*)>7;"
        cursor.execute(sql,(time_7daysago.strftime('%Y-%m-%d')))
        advertiser7 = cursor.fetchall()
        advertiser7 = DataFrame(list(advertiser7),columns=['uname','webname','week_count'])
        
        sql = "SELECT uname,webname,count(*) FROM secondHand WHERE update_time>%s GROUP BY uname,webname HAVING count(*)>30;"
        cursor.execute(sql,(time_30daysago.strftime('%Y-%m-%d')))
        advertiser30 = cursor.fetchall()
        advertiser30 = DataFrame(list(advertiser30),columns=['uname','webname','month_count'])
        
        advertiser = pd.merge(advertiser7, advertiser30, left_on = ['uname','webname'], right_on = ['uname','webname'], how = 'outer')
        advertiser = advertiser.fillna(0)
        
        for ind,ad in advertiser.iterrows():
            try:
                sql = "INSERT IGNORE INTO advertiser(uname,create_time,webname,week_count,month_count,update_time) VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(ad['uname'],cur_time,ad['webname'],int(ad['week_count']),int(ad['month_count']),cur_time))
                cursor.connection.commit()
            except BaseException as e:
                if 'Duplicate entry' in str(e):
                    sql = 'SELECT update_time from advertiser where uname=%s and webname=%s'
                    cursor.execute(sql,(ad['uname'],ad['webname']))
                    sql = "UPDATE advertiser set week_count=%s,month_count=%s,update_time=%s,update_count=update_count+1 where uname=%s and webname=%s;"
    
                    cursor.execute(sql,(int(ad['week_count']),int(ad['month_count']),cur_time.strftime('%Y-%m-%d %H:%M:%S'),ad['uname'],ad['webname']))
                    cursor.connection.commit()
                else:
                    print("["+datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"]",e)                    
    except BaseException as e:
        print("["+datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"]",e) 
        dbObject.rollback()

#%% update in secondHand
def update_ad_for_secondhand():
    try:
        cursor.execute('UPDATE secondHand SET advertiser=0 WHERE advertiser=1')
        sql = "UPDATE secondHand sh JOIN (SELECT * FROM advertiser WHERE update_time=%s) ad ON ad.uname=sh.uname and ad.webname=sh.webname SET sh.advertiser=1"
        cursor.execute(sql,cur_time.strftime('%Y-%m-%d %H:%M:%S'))
    except BaseException as e:
        print("["+datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"]",e) 


#%% main
warnings.filterwarnings('error', category=pymysql.Warning)
dbObject = dbHandle()
cursor = dbObject.cursor()
cursor.execute("USE scrapy")
cursor.execute("set names 'utf8';")
cursor.execute("set character set utf8;")
cur_time = datetime.utcnow() + timedelta(hours=8)
time_7daysago = cur_time + timedelta(days=-7)
time_30daysago = cur_time + timedelta(days=-30)
advertiser_extract()
update_ad_for_secondhand()
#cursor.close()