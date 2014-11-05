require(XLConnect)
require(plyr)


newton <- function(f, tol=1E-12,x0=1,N=20) 
{
  h <- 0.001
  i <- 1; x1 <- x0
  p <- numeric(N)
  while (i<=N) 
  {
    df.dx <- (f(x0+h)-f(x0))/h
    x1 <- (x0 - (f(x0)/df.dx))
    p[i] <- x1
    i <- i + 1
    if (abs(x1-x0) < tol) break
    x0 <- x1
  }
  return(p[1:(i-1)])
}



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
dat=data.frame()
for (l in 1:(length(lst)-4))
{
  # Rename data columns, add to dataframe dat
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

# Find delta(KWHR) values and AVG KW/DAY
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
dat <- subset(dat,dat$KW.day>0 & dat$KW.day<14000)
dat$KW.day <- as.numeric(dat$KW.day)

# fit data from turbine company to a 7th degree polynomial
pow <- data.frame('speed'=seq(0.5,20.5,0.5))
powerCurve <- c(-12,-12,-11,0,39,102,229,399,596,848,1151,1510,1938,2403,2949,3602,4306,5071,5960,6856,7849,8863,9928,10885,11619,12019,12276,12395,12449,12495,12508,12546,12555,12503,12528,12442,12396,12208,11878,11989,11495)
powerCurve.fit <- lm(powerCurve ~ poly(seq(0.5,20.5,0.5),degree = 20))

# map from power to speed
# i is index in dat
# j is index in powerCurve
for (i in 1:length(dat$KW.day))
{
  for (j in length(powerCurve))
  {
    pow.found=TRUE
    for (j in 4:(length(powerCurve)-4))
    {
      if (powerCurve[j]>dat$KW.day[i])
      {
        if(pow.found==TRUE && !(is.na(dat$KW.day[i]))) 
        {
          pow.fitSet <- c(powerCurve[(j-4):(j+4)])
          pow.xFits <- c(pow$speed[(j-4):(j+4)])
          pow.fit <- lm(pow.fitSet ~ pow.xFits)       
          # pow.pred <- predict.lm(pow.fit,x=pow.xFits)  
          write()
          fun <- function(x.guess) return(predict.lm(pow.fit,x=x.guess))
          print("hey")
          print(newton(fun, tol=1E-12,x0=1,N=20))
          dat$wind[i] <- newton(fun, tol=1E-12,x0=5,N=20) 
          
        }
        pow.found=FALSE
      }
    }
  }
}
# plot(density(dat$wind))
