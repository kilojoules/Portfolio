# Create histogram of energy generated per day density
hist(Inverter.dat$Watts,
     breaks = 200,
     xlim=c(0,11000),
     col='purple',
     xlab = 'Daily Energy Generation [W]',
     main='Data Power Density'
     )
# ----------------------------------------------------
# Wind Power Curve
powerCurve <- c(0.54,0.9,1.92,3.75,5.99,8.71,11.96,16.03,20.53,25.88,32.18,38.59,45.81,50.03)
x=seq(3,9.5,0.5)
plot(x,powerCurve,
     col="red",
     lwd = 5,
     cex=0.5,
     xlab='Wind Speed [m/s]',
     ylab='Power [kW]',
     main='Aeolos-H 50KW Wind Power Curve'
     )
# ----------------------------------------------------
# Plot average wind speed density
plot(density(Inverter.dat$wind),
     lwd=5,
     col="black",
     xlab='Wind Speed [m/s]',
     ylab = 'Probability Density',
     main='Wind Speed Density at 100 Feet'
     )
# ----------------------------------------------------
# Compare Reghleigh fit to empirical wind 
# speed distribution in April,which is 
# a month with a representative wind speed
April <- subset(Inverter.dat,month==4)
plot(density(April$extrapolated),lwd=5,
     xlab='Wind Speed [m/s]',
     main='April Wind Speed Density',
     xlim=c(0,15))
x <- density(m$extrapolated)$x
lines(x,drayleigh(x,scale = mean(April$extrapolated)),col='red',lwd=4)
legend(11,.2, # places a legend at the appropriate place 
       c("Empitical","Rayleigh"), # puts text in the legend 
       lty=c(1,1), # gives the legend appropriate symbols (lines)
       
       lwd=c(2.5,2.5),col=c("black","red"), # gives the legend lines the correct color and width
        cex=0.7 # Make the legend the right size
        )
# ----------------------------------------------------
# Compare NREL empirical density to
# Rayleigh distribution fit
x <- density(NREL.dat$avg.speed)$x
drey <- drayleigh(x,scale = mean(NREL.dat$avg.speed))
plot(density(NREL.dat$avg.speed),xlab='wind speed [m/s]',lwd = 6)
lines(x,drey,col='red',lwd=3,lty=2)
legend(13,0.1,c("Empitical","Rayleigh"),
       col=c("black","red"),
       lty=c(1,1), # gives the legend appropriate symbols (lines)
       
       lwd=c(2.5,2.5), # gives the legend lines the correct width
       cex=0.6, # Make the legend the right size
       pt.cex=1
       )

