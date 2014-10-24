require(XLConnect)
require(plyr)

# Creat Wind power curve
# ======================
# 
# Second degree polynomial fit of first 
# 7 terms of wind power curve
pow <- data.frame('speed'=seq(0.5,3.5,0.5))
pow$wpower <- c(-12,-12,-11,0,39,102,229)
pow.fit <- lm(wpower ~ poly(speed,degree = 2),dat=pow)

# Create power from curve for wind speeds 0.9
# to 20.5 at delta of 0.01
powwa <- data.frame('speed'=seq(0.9,20.5,0.01))
powwa$power <- predict.lm(pow.fit,newdata=powwa)

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
Inverter.dat$TIME <- strptime(dat$TIME, format='%Y-%m-%d')
Inverter.dat$month <- as.numeric(format(dat$TIME,'%m'))
Inverter.dat$day <- as.numeric(format(dat$TIME,'%j'))

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
        Inverter.dat$KW.day[i] <- as.numeric((Inverter.dat$DATA[i]-Inverter.dat$DATA[i-1])/as.numeric(Inverter.dat$TIME[i]-Inverter.dat$TIME[i-1]))*1000/24
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
# plot(density(dat$wind))
avg.months=data.frame('month'=c(1:12))
for (i in 1:12){
  m <- subset(dat,month==i)
  avg.months$wind.measured[i]<-mean(m$wind)
  avg.months$wind.ext[i]<-mean(m$extrapolated)
}
  
  
