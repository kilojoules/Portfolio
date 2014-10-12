# Julian Quick

# This program reads every sheet in an excel sheet
# where each sheet contains one month of cumulative power generated
# manually collected by reading the site's inverter.

# All 5 years of data are condensed to a data frame
# The power generated per day is compared to the site's
# turbine's power curve, and the distribution of average daily wind
# speed is calculated.

require(XLConnect)
require(plyr)
require('chemCal')

# Read Excel data
wb <- loadWorkbook("~/Code/RPS/BearRiverBand-Rancheria-WindTurbine-Log-2009-2014.xlsx")
lst = readWorksheet(wb, sheet = getSheets(wb))
dat=data.frame()
for (l in 1:(length(lst)-4)){
  s <- data.frame(lst[l])
  names(s) <- c('TIME','DATA','BY')
  dat <- merge(dat,s,all = TRUE)
}

# Parse timestamp
dat$TIME <- strptime(dat$TIME, format='%Y-%m-%d')
dat$month <- as.numeric(format(dat$TIME,'%m'))
dat$day <- as.numeric(format(dat$TIME,'%j'))

# Save energy data as numbers
dat$DATA <- as.numeric(dat$DATA)

# Find delta values and AVG KW/DAY
dat$KW.day <- 0
for (i in 2:length(dat$TIME))
{
  if(is.na(dat$DATA[i-1])) dat$KW.day[i] <- 0
  else
  {
    if(is.na(dat$DATA[i])) dat$KW.day[i] <- 0
    else
    {  
      if(dat$DATA[i]>dat$DATA[i-1])
      {
        dat$KW.day[i] <- as.numeric((dat$DATA[i]-dat$DATA[i-1])/as.numeric(dat$TIME[i]-dat$TIME[i-1]))
      }
      else dat$KW.day[i] <- NA
    }
  }
}

# Remove NA and inf Values. Remove mysterious 27311 and 7539
dat <- subset(dat,dat$KW.day>0 & dat$KW.day<200)
dat$KW.day <- as.numeric(dat$KW.day)

# Create density histogram. X limit is x axes limitslast value is number of bars
hist(dat$KW.day,xlim = c(0,100),100,probability = TRUE)

# data from turbine company
powerCurve <-list()
for (speed in seq(0.5,20.5,0.5))
{
  count <- as.numeric(speed*2)
  powerCurve[count] <-c(0,0,0,0,39,102,229,399,596,848,1151,1510,1938,2403,2949,3602,4306,5071,5960,6856,7849,8863,9928,10885,11619,12019,12276,12395,12449,12495,12508,12546,12555,12503,12528,12442,12396,12208,11878,11989,11495)[count]
}

# map from power to speed
for (i in 1:length(dat$KW.day))
{
  l=TRUE
  for (j in 1:length(powerCurve))
  {
    if (powerCurve[[j]]>dat$KW.day[i])
    {
      if(l==TRUE) dat$wind[i] <- (j-1)/2
      l=FALSE
    }
  }
  if (l==TRUE)
  {
    dat$wind <- 20.5
  }
}

plot(density(dat$wind))
