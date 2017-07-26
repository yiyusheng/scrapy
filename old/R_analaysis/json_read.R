# 读取json数据
scrapy_read <- function(dir_data,name){
  # 1. 文件读取
  data <- fromJSON(file = file.path(dir_data,'json',paste(name,'.json',sep='')))
  data <- data.frame(matrix(unlist(data),nrow = length(data),byrow = T))
  data$class <- name
    
  # 2. 数据预处理
  names(data) <- c('city','id','title','url','price','comment_count',
                   'img_url','time','favorite_count','desc','class')
  data$good_id <- as.character(gsub('h(.*)=','',data$url))
  col_order <- c('title','price','desc','url','good_id','time','comment_count',
                 'favorite_count','id','city','img_url','class')
  row.names(data) <- NULL
  data <- data[,col_order]
  
  # 3. 价格,评论数,收藏数数字化
  data$price <- as.numeric(levels(data$price)[data$price])
  data$favorite_count <- as.numeric(levels(data$favorite_count)[data$favorite_count])
  data$comment_count <- as.numeric(levels(data$comment_count)[data$comment_count])
  
  # 4. 删除卖两台或两台以上机器的人
  sta_id <- table(data$id)
  sta_id <- data.frame(id = names(sta_id),count = as.numeric(sta_id))
  # data <- subset(data,id %in% sta_id$id[sta_id$count <= 1])
  
  # 5. 删除重复链接
  data <- data[!duplicated(data$url),]
  data <- data[order(data$price,decreasing = T),]

  # 6. 返回值
  return(data)
}
