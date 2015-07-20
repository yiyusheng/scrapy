rm(list = ls())
require('rjson')
dir_code <- 'D:/Git/scrapy/R_analaysis'
dir_data <- 'D:/Data/scrapy'

data <- fromJSON(file = file.path(dir_data,'0720.json'))
data <- data.frame(matrix(unlist(data),nrow = length(data),byrow = T))
names(data) <- c('city','id','title','url','price','commit_count',
                 'img_url','time','favorite_count','desc')
row.names(data)
write.table(data,file = file.path(dir_data,'0720.csv'),sep=',',row.names = F)
