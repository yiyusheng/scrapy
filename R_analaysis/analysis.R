# 数据分析
rm(list = ls())
require('rjson')
dir_code <- 'D:/Git/scrapy/R_analaysis'
dir_data <- 'D:/Data/scrapy'
source(file.path(dir_code,'json_read.R'))

# 1. 读取数据
date <- '0724'
# cat <- c('lenovo','tp','wh')
cat <- 'lenovo'
suffix <- 1:10
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
data <- data[!duplicated(data$url),]
data <- data[order(data$price,decreasing = T),]
write.table(data,file = file.path(dir_data,paste(date,'.csv',sep='')),sep=',',row.names = F)
save(data,file = file.path(dir_data,paste(date,'.Rda',sep='')))
# 
# # 2. 分析
# intermatrix <- matrix(0,nrow = length(data),ncol = length(data))
# for (i in length(name):1){
#   for (j in 1:length(name)){
#     intermatrix[i,j] <- length(intersect(data[[i]]$url,data[[j]]$url))/nrow(data[[i]])
#   }
#   if (i == length(name)){
#     inter <- data[[i]]$url
#   }else  if (i >= 2){
#     inter <- intersect(data[[i]]$url,inter)
#     print(length(inter))
#   }
# }
# 
