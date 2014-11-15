#!/usr/bin/env python
# Julian Quick
from pandas import *
import matplotlib.pyplot as plt
import os
import sys

# name of plots folder
# in the form /<name>/
plotfold='plots'

# System specific info
comsep="/"
# comsep="\\"

# How many columns should I plot?
numcol=6

if len(sys.argv)>1 and sys.argv[1]=='-c':
   ylim=5000
else:ylim=1200

root = '/Users/julian/Documents/CanaryData'

for subdir, dirs, files in os.walk(root):

    # make directories for plots
    for file in dirs:
        if len(subdir.split(comsep))==3:
            try:os.mkdir(root+subdir+comsep+plotfold)
            except OSError:pass

    # plot each file
    for file in files:

        if str(file)[-4:]=='.csv' and len(subdir.split(comsep))==3:

            print 'plotting '+str(file)+'...'
            # load csv as data frame
            df=pandas.io.parsers.read_csv(subdir+comsep+file)
            for i in range(0,len(df.Timestamp)):
                df.Timestamp[i] = datetime.strptime(df.Timestamp[i], '%a %b %d %H:%M:%S %Y')

            # We only want the first 6 collumns
            df = df.ix[:,0:numcol]

            if len(sys.argv)==2:
                if sys.argv[1]=='-c':
                    df2 = df
                    df=pandas.DataFrame(df2.Timestamp)
                    df['Residence']=df2['P1rms (A)']*df2['P2rms (A)']
                    df['Specialty']=df2['P3rms (A)']*df2['P4rms (A)']

            # set up plot
            plt.figure() 
            df.plot(df.Timestamp,alpha=0.3) # add transparency to see overlapping colors
            plt.tight_layout(pad=1.08)
            plt.legend(loc='best') # add legend in non-intrusive location
            plt.legend(loc=5,prop={'size':numcol}) # 
            plt.ylabel('Current')
            plt.xlabel('Reading #')
            plt.gcf().autofmt_xdate()
            plt.gca().set_ylim([0,ylim])

            # keep plot
            spsubs = str(subdir).split(comsep)
            filnam=spsubs[0]
            for piece in range(1,len(spsubs)-1):
                filnam+='_'+spsubs[piece]
            filnam+='_'+str(file)[:-4]
            plt.savefig(root+subdir+comsep+plotfold+comsep+filnam)
