#!/usr/bin/env python
# Julian Quick
from pandas import *
import matplotlib as mpl
mpl.use('pdf')  
import matplotlib.pyplot as plt
import os
import sys
import platform
import numpy as np

# name of plots folder
plotfold='plots'

# System specific info
if platform.system()=='Darwin':comsep="/"
else: comsep="\\"

# How many columns should I plot?
numcol=6
ymin=0

if len(sys.argv)<2:
   print 'usage: ./canaryCrawler.py [-c] rootdir'
   quit()

if len(sys.argv)>2:
   ylim=1500
   root = sys.argv[2]
   if sys.argv[1]=='-f':
     ylim=10000
     ymin=-10000
else:
   ylim=1200
   root = sys.argv[1]

for subdir, dirs, files in os.walk(root):

    # plot each file
    for file in files:

        if str(file)[-4:]=='.csv': 
       
            print 'plotting '+str(file)+'...'
            # load csv as data frame
            tp=pandas.io.parsers.read_csv(subdir+comsep+file, iterator=True, chunksize=1000)
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
                        df2['Residence']=np.fft.fft(df['Residence']).real
		        df2['Specialty']=np.fft.fft(df['Specialty']).real
                        df=df2
                        print 'Fourier Transformation Complete'
                        plotfold='plots_Specialty_fft'

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

            stamp = df.Timestamp[0]
            day = datetime.strftime(stamp,'%a')
            DOM=datetime.strftime(stamp,'%d')
            month =  datetime.strftime(stamp,'%b')
            year =  datetime.strftime(stamp,'%Y')

            plt.title(subdir+'   '+day+' '+month+' '+DOM+' '+year)

            # keep plot

            # check for existing plots folder, 
            # create one if it doesn't exist
            if plotfold not in os.listdir(subdir):
                print '** adding plots directory to ',subdir
                os.mkdir(subdir+comsep+plotfold)

            # save in plots directory
            spsubs = str(subdir).split(comsep)
            filnam=''
            for piece in range(len(spsubs)-4,len(spsubs)-1):
                filnam+='_'+spsubs[piece]
            filnam+='_'+str(file)[:-4]
            saveto=subdir+comsep+plotfold+comsep+filnam
            saveto+='.pdf'
            print '**** saving plot to ',saveto
            plt.savefig(saveto)
plt.close()
