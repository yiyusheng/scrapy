# -*- coding: utf-8 -*-
import os,sys

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    dir_cookies = os.path.expanduser('~')
    cookie_path = dir_cookies + '/Data/secondHand/COOKIE_' + sys.argv[1]
    with open(cookie_path,'r') as f:
      cookie = f.read()

    trans = transCookie(cookie)
    print trans.stringToDict()
