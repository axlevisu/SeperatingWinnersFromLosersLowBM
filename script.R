#Piotroski in R
datafile <- read.csv(commandArgs(trailingOnly = FALSE)[3],sep =',',stringsAsFactors=FALSE)
useful_info <- datafile[c(3,4),]
datafile <- datafile[-(0:4),]
for(i in seq(length(datafile[,-c(1)]))){
	datafile[i,-c(1)])] <- as.numeric(datafile[i,-c(1)])
	# print(class(as.numeric(datafile[i,2])))
}
datafile[,-c(1)][is.na(datafile[,-c(1)])] <- 0
#
useful_info[1,] <- substr(useful_info[1,],nchar(useful_info[1,])-1,nchar(useful_info[1,]))
prefix_list <- levels(useful_info[1,])
levels(prefix_list) <- c('n','h','p','c','f')
adnames <- paste(prefix_list,useful_info[2])
