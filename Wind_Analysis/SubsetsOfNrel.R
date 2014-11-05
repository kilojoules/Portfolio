# 11 months of data
hist(NREL.dat$month,col='red')
axis(side=1, at=c(0:12))

summer <- subset(NREL.dat,month>=5 & month <=10)
summer.peak <- subset(summer, summer$hour>=12 & summer$hour<=17)

# hour should be greater than 8:30
summer.partial.peak <- subset(summer, format(summer$time,'%H %M')>="08 30" & format(summer$time,'%H %M')<="21 30")

# summer offpeak: 9:30pm - 8:30 am
summer.off.peak <- subset(summer, format(summer$time,'%H %M')>="21 30" | format(summer$time,'%H %M')<="08 30")

winter <- subset(NREL.dat, month<5 | month >10)

#wind partial peak: 8:30 am - 9:30 pm
winter.partial.peak <- subset(winter, format(winter$time,'%H %M')>="08 30" | format(winter$time,'%H %M')<="21 30")

#winter off peak : 9:30 pm - 8:30 am
winter.off.peak <- subset(winter, format(winter$time,'%H %M')>="21 30" | format(winter$time,'%H %M')<="08 30")

# take average wind speed for each subset
comps <- data.frame('time'=c('summer peak','summer partial peak','summer off peak','winter off peak','winter partial peak'))
comps$NREL.wind <- c(mean(summer.peak$avg.speed.150m),mean(summer.partial.peak$avg.speed.150m),mean(summer.off.peak$avg.speed.150m),mean(winter.off.peak$avg.speed.150m),mean(winter.partial.peak$avg.speed.150m))

for (i in 1:length(comps$time))
{
  # mu_sub - mu_set = k * sd(set)
  comps$k[i] <- (comps$NREL.wind[i] - mean(NREL.dat$avg.speed.150m))/sd(NREL.dat$avg.speed.150m)

  # Use K value to calculate different inverter based mean power 
  # productions for partial off and on peak
  comps$inverter.fork.sub[i] <- comps$k[i]*sd(Inverter.dat$extrapolated) + mean(Inverter.dat$extrapolated)
  comps$power.fork.sub[i] <- wpc(comps$inverter.fork.sub[i])
}
