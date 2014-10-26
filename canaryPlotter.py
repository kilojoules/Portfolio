# Julian QUick
# October 25 2014

# plots first column of csv file as x axis, next 5 columns as y axis

from pandas import *
import matplotlib.pyplot as plt

# load csv as data frame
df=pandas.DataFrame.from_csv('/Users/julian/Desktop/dat.dat')

# We only want the first 6 collumns
df = df.ix[:,1:7]

# set up plot
plt.figure(); df.plot(); plt.legend(loc='best')
plt.legend(loc=5,prop={'size':6})

# display plot
plt.show()
