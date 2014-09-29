# Julian Quick

# This program Parses an excel file, treating the first 3 columns of each sheet as part
# of the same data frame. This program outputs the contents each excel worksheet as a 
# singe csv file.

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
