require(XLConnect)
require(plyr)
wb <- loadWorkbook("~/Downloads/BearRiverBand-Rancheria-WindTurbine-Log-2009-2014.xlsx")
lst = readWorksheet(wb, sheet = getSheets(wb))

dat=data.frame()

for (l in 1:(length(lst)-4)){
  s <- data.frame(lst[l])
  names(s) <- c('TIME','DATA','BY')
  dat <- merge(dat,s,all = TRUE)
}
