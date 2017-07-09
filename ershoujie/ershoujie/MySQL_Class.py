#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filename: MySQL_Class.py
#
# Description: 
#
# Copyright (c) 2014, Yusheng Yi <yiyusheng.hust@gmail.com>
#
# Version 1.0
#
# Initial created: 2014-08-21 11:53:16
#
# Last   modified: 2015-07-26 10:24:19
#
#
#
import MySQLdb

class MC:
    user=''
    passwd=''
    host=''
    data={}

    def __init__(self,host,user,passwd):
        self.user=user
        self.host=host
        self.passwd=passwd

#connect Mysql
    def connectDB(self):
        try:
            self.conn=MySQLdb.connect(user=self.user,host=self.host,passwd=self.passwd,charset='utf8',use_unicode=False)
            self.cur=self.conn.cursor()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" %(e.args[0], e.args[1])

#select db
    def selectDB(self,db_name):
        try:
            self.conn.select_db(db_name)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" %(e.args[0], e.args[1])

#execute sql
    def executeDB(self,sql_str):
        try:
            count=self.cur.execute(sql_str)
            self.conn.commit()
            return self.cur
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" %(e.args[0], e.args[1])
#execute sql with parameter
    def executeDBp(self,sql_str,para):
        try:
            count=self.cur.execute(sql_str,para)
            self.conn.commit()
            return self.cur
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" %(e.args[0], e.args[1])

#close sql
    def closeDB(self):
        try:
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" %(e.args[0], e.args[1])
#All Done
