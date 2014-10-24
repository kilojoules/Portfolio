require(XLConnect)
require(plyr)

#==================
# Read Excel data

# Load workbook
wb <- loadWorkbook("~/Code/RPS/BearRiverBand-Rancheria-WindTurbine-Log-2009-2014.xlsx")

# loop through worksheets
lst = readWorksheet(wb, sheet = getSheets(wb))
Inverter.dat=data.frame()
for (l in 1:(length(lst)-4))
{
  # Rename data columns, add to dataframe dat
  s <- data.frame(lst[l])
  names(s) <- c('TIME','DATA','BY')
  Inverter.dat <- merge(Inverter.dat,s,all = TRUE)
}

# Parse timestamp
Inverter.dat$TIME <- strptime(Inverter.dat$TIME, format='%Y-%m-%d')
Inverter.dat$month <- as.numeric(format(Inverter.dat$TIME,'%m'))
Inverter.dat$day <- as.numeric(format(Inverter.dat$TIME,'%j'))

# Save energy data as numbers
Inverter.dat$DATA <- as.numeric(Inverter.dat$DATA)

# Find delta(KWHR) values and AVG KW/DAY
Inverter.dat$KW.day <- 0
for (i in 2:length(Inverter.dat$TIME))
{
  if(is.na(Inverter.dat$DATA[i-1])) Inverter.dat$KW.day[i] <- 0
  else
  {
    if(is.na(Inverter.dat$DATA[i])) Inverter.dat$KW.day[i] <- 0
    else
    {  
      if(Inverter.dat$DATA[i]>Inverter.dat$DATA[i-1])
      {
        # Assume inverter effeciency is 0.927
        Inverter.dat$KW.day[i] <- (1/0.927)*as.numeric((Inverter.dat$DATA[i]-Inverter.dat$DATA[i-1])/as.numeric(Inverter.dat$TIME[i]-Inverter.dat$TIME[i-1]))*1000/24
      }
      else Inverter.dat$KW.day[i] <- NA
    }
  }
}

# Remove NA and inf Values. Remove mysterious 27311 and 7539
Inverter.dat <- subset(Inverter.dat,Inverter.dat$KW.day>0 & Inverter.dat$KW.day<14000)
Inverter.dat$KW.day <- as.numeric(Inverter.dat$KW.day)

# fit data from turbine company to a 7th degree polynomial
powerCurve <- c(-12,-12,-11,0,39,102,229,399,596,848,1151,1510,1938,2403,2949,3602,4306,5071,5960,6856,7849,8863,9928,10885,11619,12019,12276,12395,12449,12495,12508,12546,12555,12503,12528,12442,12396,12208,11878,11989,11495)
powerCurve.fit <- lm(powerCurve ~ poly(seq(0.5,20.5,0.5),degree = 20))
powwa <- data.frame('speed'=seq(0.9,20.5,0.01))
powwa$power <- predict.lm(pow.fit,newdata=powwa)

# map from power to speed
for (i in 1:length(Inverter.dat$KW.day))
{
  l=TRUE
  for (j in 1:length(powwa$power))
  {
    if (powwa$power[j]>Inverter.dat$KW.day[i])
    {
      if(l==TRUE) Inverter.dat$wind[i] <- 0.9 + 0.01*j
      l=FALSE
    }
  }
  if (l==TRUE)
  {
    Inverter.dat$wind <- 20.5
  }
}

# extrapolate to new height
newHeight=150
Inverter.dat$extrapolated <- Inverter.dat$wind * (newHeight/100)^(1/7)

# find monthly averages
avg.months=data.frame('month'=c(1:12))
for (i in 1:12){
  m <- subset(Inverter.dat,month==i)
  avg.months$wind.measured[i]<-mean(m$wind)
  avg.months$wind.ext[i]<-mean(m$extrapolated)
}


avg.invmonths=data.frame('month'=c(1:12))
for (i in 1:12)
{
  # make subset
  m <- subset(Inverter.dat,month==i)
  
  # record average measured and extrapolated speeds
  avg.invmonths$wind.measured[i]<-mean(m$wind)
  avg.invmonths$wind.ext[i] <- mean(m$extrapolated)
  
  # Find monthly extrapolated power
  x <- density(m$extrapolated)$x
  drey <- density(drayleigh(x,scale = mean(m$extrapolated)))
  pow <- drey$y*(drey$x[4]-drey$x[3])*wpc(x)
  avg.invmonths$power.ext[i] <- sum(pow)
  avg.invmonths$low[i] <- sum(pow) * 0.99
  avg.invmonths$high[i] <- sum(pow) * 1.01
}


