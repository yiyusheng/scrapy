import os
import string

str_execu = 'scrapy crawl ershoujie -o 0724lenovo'
str_execu = [str_execu + `i` + '.json' for i in range(1,11)]

for cmd in str_execu:
    print(cmd)
    os.system(cmd)
