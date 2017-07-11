rm(list = ls());setwd('/home/yiyusheng/Code/Python/scrapy/R_analaysis/');source('~/rhead')
require('rjson')
dir_data <- '/home/yiyusheng/Data/scrapy'

read_deyi <- function(dname){
  dir_scrapy <- file.path(dir_data,dname)
  fname <- list.files(dir_scrapy)
  fname <- fname[grepl('20.*-.*-.*',fname)]
  r <- lapply(fname,function(fn){
    DT <- read.csv(file.path(dir_scrapy,fn))
  })
  DT <- do.call(rbind,r)
  DT <- DT[!duplicated(DT[,c('url','title')]),]
  save(DT,file = file.path(dir_data,'Rda',paste(dname,'.Rda',sep='')))
  return(DT)
}

deyiM <- read_deyi('deyiMobi')
deyiW <- read_deyi('deyiWeb')
dgtleW <- read_deyi('dgtleWeb')

get_dupItem <- function(DT){
  dupUrl <- DT$url[duplicated(DT$url)]
  return(factorX(subset(DT,url %in% dupUrl)))
}
