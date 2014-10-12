# Julian Quick

# This program processes data NREL collected
# then predicts the site power generation distribution
# using a 10 kW turbine power curve

# for every file in directory "/Users/julian/Code/RPS/NREL Data/" with RV in the name
# save info to data frame "dat"
dat=data.frame()
i=1
for (file in list.files('/Users/julian/Code/RPS/NREL Data',pattern = 'RV',full.names=TRUE)) 
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
  dat<-merge(a,dat,all=TRUE)
}

# parse timestamp
dat$time <- strptime(dat$time, format='%m/%d/%Y %H:%M')

# map from 20m to 150m
dat$avg.speed.150m=dat$avg.speed*(150/20)^(1/7)

# powerCurve is structure such that index = speed*2+2
powerCurve <-list()
for (speed in seq(0.5,20.5,0.5))
{
  count <- as.numeric(speed*2)
  
  # this is the data from the turbine company
  powerCurve[count] <-c(0,0,0,0,39,102,229,399,596,848,1151,1510,1938,2403,2949,3602,4306,5071,5960,6856,7849,8863,9928,10885,11619,12019,12276,12395,12449,12495,12508,12546,12555,12503,12528,12442,12396,12208,11878,11989,11495)[count]
}

# map through wind power curve
for (i in seq(1,length(dat$avg.speed.150m)))
{
  if(dat$avg.speed.150m[i]>20)
  {
    dat$power[i] <- 11495
  }
  else 
  {
    if(dat$avg.speed.150m[i]<2)
    {
      dat$power[i] <- 0
    }
    else
    {
      dat$power[i] <- powerCurve[[round(dat$avg.speed.150m[i]*2-2)]]
    }
  }
}

plot(ecdf(dat$power))
plot(density(dat$power))
