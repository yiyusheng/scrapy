rm(list = ls())
require('rjson')
dir_code <- 'D:/Git/scrapy/R_analaysis'
dir_data <- 'D:/Data/scrapy'

data <- fromJSON(file = file.path(dir_data,'0720.json'))
data <- data.frame(matrix(unlist(data),nrow = length(data),byrow = T))
names(data) <- c('city','id','title','url','price','commit_count',
                 'img_url','time','favorite_count','desc')
col_order <- c('title','price','time','commit_count','favorite_count','id','city',
               'desc','url','img_url')
row.names(data)
data <- data[,col_order]

data$price <- as.numeric(levels(data$price)[data$price])

data.tp <- subset(data,(grepl('think',title) | grepl('think','desc')) & price > 500)
data.tp <- data.tp[order(data.tp$price),]
write.table(data.tp,file = file.path(dir_data,'0720.csv'),sep=',',row.names = F)