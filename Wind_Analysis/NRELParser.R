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
  a[2] <- s[2]
  a[3] <- s[3]
  a[4] <- s[4]
  names(a) <- c('time','avg.speed','sd','avg.dir')
  NREL.dat<-merge(a,NREL.dat,all=TRUE)
}

# parse timestamp
NREL.dat$time <- strptime(NREL.dat$time, format='%m/%d/%Y %H:%M')
NREL.dat$month <- as.numeric(format(NREL.dat$time,format = '%m'))
NREL.dat$hour <- as.numeric(format(NREL.dat$time,format='%H'))

# map 
NREL.dat$avg.speed.150m=NREL.dat$avg.speed*(100/60)^(1/7)

# powerCurve is structure such that index = speed*2+2
powerCurve <-list()
for (speed in seq(0.5,20.5,0.5))
{
  count <- as.numeric(speed*2)
  
  # this is the NREL.data from the turbine company
  powerCurve[count] <-c(0,0,0,0,39,102,229,399,596,848,1151,1510,1938,2403,2949,3602,4306,5071,5960,6856,7849,8863,9928,10885,11619,12019,12276,12395,12449,12495,12508,12546,12555,12503,12528,12442,12396,12208,11878,11989,11495)[count]
}

# map through wind power curve
for (i in seq(1,length(NREL.dat$avg.speed.150m)))
{
  if(NREL.dat$avg.speed.150m[i]>20)
  {
    NREL.dat$power[i] <- 11495
  }
  else 
  {
    if(NREL.dat$avg.speed.150m[i]<2)
    {
      NREL.dat$power[i] <- 0
    }
    else
    {
      NREL.dat$power[i] <- powerCurve[[round(NREL.dat$avg.speed.150m[i]*2-2)]]
    }
  }
}

plot(ecdf(NREL.dat$power))
hist(density(NREL.dat$avg.speed))

# Compare rayleigh to actual NREL NREL.data
require('VGAM')
vars <-data.frame('month'=seq(1,12))
for (i in 1:12)
{
  feb <- subset(NREL.dat,NREL.dat$month==i)
  vars$vars[i]<-var(drayleigh(density(feb$avg.speed)$x,scale=mean(feb$avg.speed)),density(feb$avg.speed)$y)
}

avg.months=data.frame('month'=c(1:12))
for (i in 1:12)
{
  # make subset
  m <- subset(NREL.dat,month==i)
  
  # record average measured and extrapolated speeds
  avg.months$wind.measured[i]<-mean(m$avg.speed)
  avg.months$wind.ext[i]<-mean(m$avg.speed.150m)
  
  # Find monthly extrapolated power)
  avg.months$power.ext <- wpc(avg.months$wind.ext)
}






