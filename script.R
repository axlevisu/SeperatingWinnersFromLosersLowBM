#Piotroski in R
datafile <- read.csv(commandArgs(trailingOnly = FALSE)[6],sep =',',stringsAsFactors=FALSE)
useful_info <- datafile[c(3,4),-c(1)]
datafile <- datafile[-(0:4),]
names <- t(datafile[,1])
datafile <- datafile[,-c(1)]
datafile <- as.data.frame(sapply(datafile,as.numeric))
datafile[is.na(datafile)] <- 0
rownames(datafile) <- names
useful_info[1,] <- substr(useful_info[1,],nchar(useful_info[1,])-1,nchar(useful_info[1,]))
prefix_list <- levels(useful_info[1,])
levels(prefix_list) <- c('n','h','p','c','f')
adnames <- paste(prefix_list,useful_info[2])
