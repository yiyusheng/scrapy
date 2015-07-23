rm(list = ls())
require('rjson')
require('ggplot2')
dir_code <- 'D:/Git/scrapy/R_analaysis'
dir_data <- 'D:/Data/scrapy'

# 1. 读取数据
date <- '0723'
cat <- c('lenovo','tp','wh')
name <- paste(date,cat,sep = '')

data <- fromJSON(file = file.path(dir_data,paste(name[1],'.json',sep='')))
data <- data.frame(matrix(unlist(data),nrow = length(data),byrow = T))
data$class <- cat[1]
for (i in 2:length(name)){
  d <- fromJSON(file = file.path(dir_data,paste(name[i],'.json',sep='')))
  d <- data.frame(matrix(unlist(d),nrow = length(d),byrow = T))
  d$class <- cat[i]
  data <- rbind(data,d)
}

# 2. 数据预处理
names(data) <- c('city','id','title','url','price','comment_count',
                 'img_url','time','favorite_count','desc','class')
col_order <- c('title','price','desc','url','time','comment_count',
               'favorite_count','id','city','img_url')
row.names(data) <- NULL
data <- data[,col_order]

# 3. 价格,评论数,收藏数数字化
data$price <- as.numeric(levels(data$price)[data$price])
data$favorite_count <- as.numeric(levels(data$favorite_count)[data$favorite_count])
data$comment_count <- as.numeric(levels(data$comment_count)[data$comment_count])


# 4. 删除卖两台或两台以上机器的人
sta_id <- table(data$id)
sta_id <- data.frame(id = names(sta_id),count = as.numeric(sta_id))
data <- subset(data,id %in% sta_id$id[sta_id$count <= 2])

# 5. 存储
data <- data[order(data$price,decreasing = T),]
write.table(data,file = file.path(dir_data,paste(date,'.csv',sep='')),sep=',',row.names = F)