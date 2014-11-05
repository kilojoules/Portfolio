Power2 <- function(v)
{
  powerCurve <- c(0.54,0.9,1.92,3.75,5.99,8.71,11.96,16.03,20.53,25.88,32.18,38.59,45.81,50.03,50,50,50,50)
  x=seq(3,11.5,0.5)
  surr=3 # number of surrounding points
  
  # return NA if NA
  if (is.na(v))return(NA)
  
  # which power curve value are we closest to?
  # binned by .5 m/s, so multiply v by 2
  # starts at 3 m/a so subtract 2
  indexx= 2*(v-2) - 1 # curve is binned by 0.5 m/s
  
  #Low speeds dismissed
  if (v <=3.0)return(0)
  
  # speeds beyond curve correspond to 50
  if (v>length(powerCurve)/2)return(50)
  
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
  pred <- lm(powerCurve[rang] ~ poly(speed,degree=3),data=powwa)
  pows$power <- predict(pred,newdata=pows)
  return(pows$power)
}

wpc2 <- function(dats)
{
  s <- data.frame('s'=c(1:length(dats)))
  for (i in 1:length(dats))
  {
    s$s[i] <- Power2(dats[i])
  }
  return(s$s)
}
