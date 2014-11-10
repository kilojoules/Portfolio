#!/usr/bin/env python
# Julian Quick
from pandas import *
import matplotlib.pyplot as plt
import os

# name of plots folder
# in the form /<name>/
plotfold='plots'

# How many columns should I plot?
numcol=6

for subdir, dirs, files in os.walk('35ca7'):

    # make directories for plots
    for file in dirs:
        if len(subdir.split('/'))==3:
            try:os.mkdir(subdir+'/'+plotfold)
            except OSError:pass

    # plot each file
    for file in files:

        print 'plotting from ',subdir,str(file)
        if str(file)[-4:]=='.csv' and len(subdir.split('/'))==3:

            # load csv as data frame
            df=pandas.io.parsers.read_csv(subdir+'/'+file)

            # We only want the first 6 collumns
            df = df.ix[:,0:numcol]

            # set up plot
            plt.figure() 
            df.plot(df.Timestamp,alpha=0.3) # add transparency to see overlapping colors
            plt.legend(loc='best') # add legend in non-intrusive location
            plt.legend(loc=5,prop={'size':numcol}) # 
            plt.ylabel('Current')
            plt.xlabel('Reading #')
            plt.gcf().autofmt_xdate()

            # display plot
            spsubs = str(subdir).split('/')
            filnam=spsubs[0]
            for piece in range(1,len(spsubs)-1):
                filnam+='_'+spsubs[piece]
            filnam+='_'+str(file)[:-4]
            plt.savefig(subdir+'/'+plotfold+'/'+filnam)
