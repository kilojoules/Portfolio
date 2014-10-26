# Julian QUick
# October 25 2014

# plots first column of csv file as x axis, next 5 columns as y axis

from pandas import *
import matplotlib.pyplot as plt
import sys

# load csv as data frame
df=pandas.io.parsers.read_csv(str(sys.argv[1]))

# We only want the first 6 collumns
df = df.ix[:,0:6]

# set up plot
plt.figure() 
df.plot(alpha=0.3)
plt.legend(loc='best')
plt.legend(loc=5,prop={'size':6})

# display plot
plt.show()
