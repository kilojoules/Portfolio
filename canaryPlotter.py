#!/usr/bin/env python
# Julian Quick
# plots first column of csv file as x axis, next 5 columns as y axis

from pandas import *
import matplotlib.pyplot as plt
import sys

# This program needs a csv file to plot
# which must be specified in the command line
# Ex. ./canaryPlotter.py dat.dat
if len(sys.argv)!=2:
  print "please specify csv file to plot"
  quit()

# load csv as data frame
df=pandas.io.parsers.read_csv(str(sys.argv[1]))

# How many columns should I plot?
numcol=6

# We only want the first 6 collumns
df = df.ix[:,0:numcol]

# set up plot
plt.figure() 
df.plot(alpha=0.3) # add transparency to see overlapping colors
plt.legend(loc='best') # add legend in non-intrusive location
plt.legend(loc=5,prop={'size':numcol}) # 
plt.ylabel('Current')
plt.xlabel('Reading #')

# display plot
plt.show()
