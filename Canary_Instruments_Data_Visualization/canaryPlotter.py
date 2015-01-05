#!/usr/bin/env python
# Julian Quick
# plots first column of csv file as x axis, next 5 columns as y axis

from pandas import *
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import os
import sys 
import platform
import numpy as np


# Default name of plots folder
plotfold='plots'

# Initial parameterization
numcol=6
ymin=0

if len(sys.argv)<2:
   print 'usage: ./canaryCrawler.py [-c] rootdir'
   quit()

if len(sys.argv)>2:
   ylim=500
   root = sys.argv[2]
   if sys.argv[1]=='-f':
     ylim=10000
     ymin=-10000
else:
   ylim=1200
   root = sys.argv[1]

file = root
print 'plotting '+str(file)+'...'
# load csv as data frame
tp=pandas.io.parsers.read_csv(root, iterator=True, chunksize=1000)
df = concat(tp, ignore_index=True)
for i in range(0,len(df.Timestamp)):
  df.Timestamp[i] = datetime.strptime(df.Timestamp[i], '%a %b %d %H:%M:%S %Y')
  
# We only want the first 6 collumns
df = df.ix[:,0:numcol]

if len(sys.argv)>2:
  df2 = df
  del df
  df=pandas.DataFrame(df2.Timestamp)
  if sys.argv[1]=='-c' or sys.argv[1]=='-f':
    plotfold='plots_Specialty'
    df['Residence']=df2['P1rms (A)']+df2['P2rms (A)']
    df['Specialty']=df2['P3rms (A)']+df2['P4rms (A)']
    if sys.argv[1]=='-f':
	df2=pandas.DataFrame(df.Timestamp)
	df2['Residence']=np.fft.fft(df['Residence'])
	df2['Specialty']=np.fft.fft(df['Specialty'])
	df=df2
	print 'Fourier Transformation Complete'
	plotfold='plots_Specialty_fft'

	threedee = plt.figure().gca(projection='3d')
	threedee.scatter(df.index, df['Residence'].real, df['Residence'].imag)
	threedee.set_xlabel('index')
	threedee.set_ylabel('real')
	threedee.set_zlabel('complex')

	plt.show()
	quit()

# set up plot
plt.figure()
df.plot(df.Timestamp,alpha=0.6,linewidth=2.3) # add transparency to see overlapping colors
plt.tight_layout(pad=1.08)
plt.legend(loc='best') # add legend in non-intrusive location
plt.legend(loc=5,prop={'size':14}) # 
plt.ylabel('Current')
plt.xlabel('Time')
plt.gcf().autofmt_xdate()
plt.gcf().set_size_inches(12.7,9.2)
plt.gca().set_ylim([ymin,ylim])

plt.title(root)

plt.show()


