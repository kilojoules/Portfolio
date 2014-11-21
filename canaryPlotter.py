#!/usr/bin/env python
# Julian Quick
# plots first column of csv file as x axis, next 5 columns as y axis

from pandas import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import sys

# This program needs a csv file to plot
# which must be specified in the command line
# Ex. ./canaryPlotter.py dat.dat
if len(sys.argv)<2:
  print "please specify csv file to plot"
  quit()

# load csv as data frame
df=pandas.io.parsers.read_csv(str(sys.argv[1]))#,keep_date_col=True)
for i in range(0,len(df.Timestamp)):
   df.Timestamp[i] = datetime.strptime(df.Timestamp[i], '%a %b %d %H:%M:%S %Y')

# How many columns should I plot?
numcol=6

# We only want the first 6 collumns
df = df.ix[:,0:numcol]

if len(sys.argv)==3:
   if sys.argv[2]=='-c':
      df2 = df
      df=pandas.DataFrame(df2.Timestamp)
      df['Residence']=df2['P1rms (A)']*df2['P2rms (A)']
      df['Specialty']=df2['P3rms (A)']*df2['P4rms (A)']


# set up plot
plt.figure() 
# matplotlib.dates.AutoDateLocator()
df.plot(df.Timestamp,linewidth=2.3) # add transparency to see overlapping colors
plt.plot()
plt.legend(loc='best') # add legend in non-intrusive location
plt.tight_layout(pad=1.08)
plt.legend(loc=5,prop={'size':14}) # 
plt.gcf().set_size_inches(12.7,9.2)
plt.ylabel('Current')
plt.xlabel('Date')

plt.gcf().autofmt_xdate()

if len(sys.argv)==2:
   plt.gca().set_ylim([0,1200])

else: plt.gca().set_ylim([0,5000])

stamp = df.Timestamp[0]
day = datetime.strftime(stamp,'%a')
DOM=datetime.strftime(stamp,'%d')
month =  datetime.strftime(stamp,'%b')
year =  datetime.strftime(stamp,'%Y')

plt.title(day+' '+month+' '+DOM+' '+year)
plt.show()

