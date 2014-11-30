require(VGAM)
NREL.dat=data.frame()

# for every file in directory "/Users/julian/Code/RPS/NREL NREL.data/" with RV in the name
# save info to NREL.data frame "NREL.dat"
i=1
for (file in list.files('/Users/julian/Code/RPS/NREL data',pattern = 'RV',full.names=TRUE)) 
{
  s <-data.frame(read.csv(file,skip = 55,sep='\t',header=TRUE))
  if(length(s)==1)
  {
    s <-data.frame(read.csv(file,skip = 55,sep=',',header=TRUE))
  }
  a <- data.frame(s[1])
  
  # either units == 'm/s', or units (a[2])
  # is in mph
  lin <- readLines(file)[32]
  if (grepl('m/s',lin))
  {
    a[2] <- s[2]
    # print('m/s')
  }else if (grepl('mph',lin))
  {
    a[2] <- 0.44704*s[2]
    # print('other')
  }else print(c('error on file',file,'no units found'))
  a[3] <- s[3]
  a[4] <- s[4]
  names(a) <- c('time','avg.speed','sd','avg.dir')
  NREL.dat<-merge(a,NREL.dat,all=TRUE)
}

# Remove NA values
NREL.dat <- subset(NREL.dat, 
                   !is.na(time)
)

# parse timestamp
NREL.dat$time <- strptime(NREL.dat$time, format='%m/%d/%Y %H:%M')
NREL.dat$month <- as.numeric(format(NREL.dat$time,format = '%m'))
NREL.dat$hour <- as.numeric(format(NREL.dat$time,format='%H'))
NREL.dat$minute <- as.numeric(format(NREL.dat$time,format='%M'))
NREL.dat$day <- as.numeric(format(NREL.dat$time,format = '%j'))

# map from 60 feet to 170 feet
NREL.dat$avg.speed.150m=NREL.dat$avg.speed*(170/60)^(1/7)

# time of use sceme: mean(set)-mean(subet) = K sd(set)
avg.months=data.frame('month'=c(1:12))
for (i in 1:12)
{
  # make subset
  m <- subset(NREL.dat,month==i)
  if(length(m$time)>0)
  {
    # record average measured and extrapolated speeds
    avg.months$wind.measured[i]<-mean(m$avg.speed)
    avg.months$wind.ext[i]<-mean(m$avg.speed.150m)
    
    # Find monthly extrapolated power)
    avg.months$power.ext[i] <- mean(wpc2(m$avg.speed.150m))
  }
}

