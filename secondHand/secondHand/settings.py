# -*- coding: utf-8 -*-

# Scrapy settings for secondHand project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'secondHand'

SPIDER_MODULES = ['secondHand.spiders']
NEWSPIDER_MODULE = 'secondHand.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'secondHand (+http://www.yourdomain.com)'
#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'  

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIE_stage1st = {'B7Y9_2132_myrepeat_rr': 'R0', 'B7Y9_2132_forum_lastvisit': 'D_115_1546586268', 'B7Y9_2132_pc_size_c': '0', 'B7Y9_2132_lastact': '1546586269%09home.php%09spacecp\n', 'B7Y9_2132_sid': 'CHhO3n', 'B7Y9_2132_st_t': '492139%7C1546586268%7C66ff86f67c5c8f2ed01a9daea39ad2a1', 'CNZZDATA1260281688': '1337231653-1541502892-https%253A%252F%252Fwww.google.com%252F%7C1546583240', 'B7Y9_2132_lastvisit': '1546582612', 'B7Y9_2132_lip': '192.168.1.173%2C1546586205', 'B7Y9_2132_saltkey': 'LIBG9zqQ', '_uab_collina': '154150623676351154267279', 'B7Y9_2132_auth': '2546wMH3X9W37P88hIlDhmcy%2B4mEn%2F9%2Fh0tVOUNmoHM%2Fhgdhettk8NwglmIvskzJoyYgMgngmM0iXq7gx41I%2FSGSDUY', 'B7Y9_2132_yfe_in': '1', 'B7Y9_2132_lastcheckfeed': '492139%7C1546586266', 'B7Y9_2132_ulastactivity': 'e43f4TnP1H2vTCq%2FDYohzM%2Fg0X8B0JWNDGXyTpYg6f%2FE1pI%2FarFC', 'UM_distinctid': '166e8ee8d0c770-04db571e1916e-1e386652-fa000-166e8ee8d0d2eb', 'B7Y9_2132_sendmail': '1', 'B7Y9_2132_visitedfid': '115', '__cfduid': 'd278021177f7a6ead6ca597ea9e63fba71541129510'}

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'secondHand.middlewares.SecondhandSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'secondHand.rotate_useragent.RotateUserAgentMiddleware': 100,
    'secondHand.middlewares.JavaScriptMiddleware':101
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'secondHand.pipelines.SecondhandPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
LOG_LEVEL = 'WARNING'
