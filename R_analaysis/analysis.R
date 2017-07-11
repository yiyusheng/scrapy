# 数据分析
rm(list = ls());setwd('/home/yiyusheng/Code/Python/scrapy/R_analaysis/');source('~/rhead')
require('rjson')
source('json_read.R')

# 1. 读取数据
date <- '0723'
# cat <- c('lenovo','tp','wh')
cat <- 'lenovo'
suffix <- ''
name <- paste(date,cat,suffix,sep = '')

data_list <- list()
for (i in 1:length(name)){
  d <- scrapy_read(dir_data,name[i])
  data_list[[name[i]]] <- d
  if (i == 1)
    data <- d
  else
    data <- rbind(data,d)
  
}

# 2. 存储
data <- data[!duplicated(data$good_id),]
data <- data[order(data$price,decreasing = T),]
write.table(data,file = file.path(dir_data,paste(date,'.csv',sep='')),sep=',',row.names = F)
save(data,file = file.path(dir_data,paste(date,'.Rda',sep='')))

# 3. 读取
load(file = file.path(dir_data,'0723.Rda'))
d1 <- data
load(file.path(dir_data,'0724.Rda'))
d2 <- data
data <- rbind(d1,d2)
data <- data[!duplicated(data$good_id),]
data <- data[order(data$good_id),]
write.table(data,file = file.path(dir_data,'all.csv'),sep=',',row.names = F)

