#!/usr/bin/env python2

# output all data in MySQL
import ershoujie.MySQL_Class as mc
import csv
import os

# parameter
outfile = 'ershoujie.csv'
os.system('scrapy crawl ershoujie')

# MySQL config
host = 'localhost'
user = 'root'
passwd = 'qwer1234'

# DB info
DB = 'scrapy'
Table = 'ershoujie'

# DB exec
ms = mc.MC(host,user,passwd)
ms.connectDB()
ms.selectDB(DB)

# fetch data
sqlstr = '''select * from %s.%s''' %(DB,Table)
r = ms.executeDB(sqlstr)
r = r.fetchall()

# write outfile
with open(outfile,'wb') as f:
    fw = csv.writer(f,delimiter = ',')
    fw.writerows(r)
