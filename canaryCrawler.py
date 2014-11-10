#!/usr/bin/env python
# Julian Quick
from pandas import *
import matplotlib.pyplot as plt
import os

# name of plots folder
# in the form /<name>/
plotfold='plots'

for subdir, dirs, files in os.walk('Your_Folder'):

    # make directories for plots
    for file in dirs:
        if len(subdir.split('/'))==4:
            try:os.mkdir(subdir+'/'+plotfold)
            except OSError:pass

    # plot each file
    for file in files:

        if str(file)[-4:]=='.csv' and len(subdir.split('/'))==4:

            # load csv as data frame
            df=pandas.io.parsers.read_csv(subdir+'/'+file)

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
            spsubs = str(subdir).split('/')
            filnam=spsubs[0]
            for piece in range(1,len(spsubs)-1):
                filnam+='_'+spsubs[piece]
            filnam+='_'+str(file)[:-4]
            plt.savefig(subdir+'/'+plotfold+'/'+filnam)
