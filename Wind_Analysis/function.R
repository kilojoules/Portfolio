Power <- function(v)
{
    powerCurve <- c(-12,-12,-11,0,39,102,229,399,596,848,1151,1510,1938,2403,2949,3602,4306,5071,5960,6856,7849,8863,9928,10885,11619,12019,12276,12395,12449,12495,12508,12546,12555,12503,12528,12442,12396,12208,11878,11989,11495)
    x=seq(0.5,20.5,0.5)

    # speeds less than or equal to 2 m/s dismissed
    if (v <=2)return(0)
    if (v >17)return(11495)
    if (is.na(v))return(NA)
    # make polynomial fit with surrounding curve points
    surr=3 # number of surrounding points
    indexx= v*2 # curve is binned by 0.5 m/s
    rang <- (indexx-surr):(indexx+surr)
    powwa <- data.frame('speed'=x[rang])
    pows <- data.frame('speed'=v)
    pred <- lm(powerCurve[rang] ~ poly(speed,degree=6),data=powwa)
    pows$power <- predict(pred,newdata=pows)
    return(pows$power)
}

dfram <- data.frame('x'=c(1,2,3,4))
dfram$y <- c(1,4,9,16)

pred <- data.frame('x'=c(5,6))
# pred$y <- predict using trent in dfram

wpc <- function(dats)
{
  s <- data.frame('s'=c(1:length(dats)))
  for (i in 1:length(dats))
  {
    s$s[i] <- Power(dats[i])
  }
  return(s$s)
}

