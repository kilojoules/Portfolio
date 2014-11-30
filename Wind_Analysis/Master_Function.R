Powerm <- function(v,turbnum)
# This function inputs wind speed (m/s) and a specified turbine,
# then outputs the turbine's rated power
# v is wind speed
# turbnuum is turbine analyzed
  # 
{
  # turnine 1 is 10 kW bergy
  if (turbnum ==1)
  {
    powerCurve <- c(-12,-12,-11,0,39,102,229,399,596,848,1151,1510,1938,2403,2949,3602,4306,5071,5960,6856,7849,8863,9928,10885,11619,12019,12276,12395,12449,12495,12508,12546,12555,12503,12528,12442,12396,12208,11878,11989,11495)
    x=seq(0.5,20.5,0.5)
    indexx= 2*v # curve is binned by 0.5 m/s
  }
  
  # Turbine 2 is Aeolos-H 50 kW
  if (turbnum == 2) 
  {
    powerCurve <- c(0.54,0.9,1.92,3.75,5.99,8.71,11.96,16.03,20.53,25.88,32.18,38.59,45.81,50.03,50,50,50,50)
    x=seq(3,11.5,0.5)
    
    # which power curve value are we closest to?
    # binned by .5 m/s, so multiply v by 2
    # starts at 3 m/a so subtract 2
    indexx= 2*(v-2) - 1 # curve is binned by 0.5 m/s
  }
  
  # turnine 3 is 50 kW Endurance #-3120
  # http://www.smallwindcertification.org/wp-content/new-uploads/2013/11/SPP-13-07-Summary-Report.pdf
  if (turbnum ==3)
  {
    powerCurve <- c(-0.14,-.33,-.24,-0.09,1.03,2.48,4.71,8.21,11.82,16.19,20.17,25.04,29.26,35.07,36.69,43.96,46.67,51.52,54.73,56.84,58.92,60.25,61.25,62.1,62.67,63.38,63.62,65.02,65.47,65.67,66.57)
    x=seq(1.5,16.5,0.5)
    indexx= 2*v-1 # curve is binned by 0.5 m/s
  }
  
  # Turbine 4 is Northern 100 kW
  if (turbnum == 4) 
  {
    powerCurve <- c(-.5,-.5,1.2,7.2,14.5,24.7,37.9,58.7,74.8,85.1,90.2,94.7,95.3,95.1,94.2,92.9,91.2,88.9,87.1,84.1,81.3,78.6,76.1,74.3,71.1)
    x=seq(1,25,1)
    indexx=v
  }
  
  # surr is the number of surrounding 
  # points in polynomial approximation.
  surr=2
  
  # return NA if NA
  if (is.na(v))return(NA)
  
   
  #Low speeds dismissed
  if (v < 3)return(0)
  
  # speeds beyond curve correspond to 50
  if (v>tail(x,1))return(tail(powerCurve,1))
  
  # determine appropriate extrapolation region.
  
  # If wind speed is at the end of the power curve, 
  # don't fit to the right of it.
  if (indexx>=length(powerCurve)-surr) 
  {
    rang <- (indexx-surr):length(powerCurve)
  }
  
  # same logic but for low wind speeds
  else if (indexx<=surr)
  {
    rang <-1:(indexx+surr)
  }
  
  # everythin's fine, no special case
  else 
  { 
    rang <- (indexx-surr):(indexx+surr) 
  }
  
  # make polynomial fit with surrounding curve points
  powwa <- data.frame('speed'=x[rang])
  pows <- data.frame('speed'=v)
  pred <- lm(powerCurve[rang] ~ poly(speed,degree=length(unique(powwa$speed))-1),data=powwa)
  pows$power <- predict(pred,newdata=pows)
  if (pows$power[1]<0) return(0)
  return(pows$power)
}

wpcm <- function(dats,turbnum)
{
  s <- data.frame('s'=c(1:length(dats)))
  for (i in 1:length(dats))
  {
    s$s[i] <- Powerm(dats[i],turbnum)
  }
  return(s$s)
}

