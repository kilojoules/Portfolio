#!/usr/bin/env python
# Julian Quick
# Crawls through input root directory
# and creates static plots of data
# usage: ./canaryCrawler.py [-c or -f] root_dir/ [-o]
#   -c: plot combined residential and specialty signals
#   -f: create 3d plots of fft results
#   -o: Overwrite existing plots
from pandas import *
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
mpl.use('pdf')  
import matplotlib.pyplot as plt
import os
import sys
import platform
import numpy as np
import math

def calcurv(x, col):

   if type(x) is pandas.tslib.Timestamp:return x
   if col == 1:
      a,b,c,d,e = (29, 0.0402, 0.0944, 1.2259, 3.1254)
   elif col == 2:
      a,b,c,d,e = (29, 0.0400, 0.1098, 1.3221, 3.4830)
   elif col == 3:
      a,b,c,d,e = (33, 0.0237, 0.0218, 0.7964, 2.0601)
   elif col == 4:  
      a,b,c,d,e = (33, 0.0236, 0.0187, 0.8086, 2.1167)
   elif col == 5:
      a,b,c,d,e = (33, 0.0237, 0.0226, 0.7884, 2.0423)

   if x <=a: y = b*x - c
   else: y = d*math.log(x) - e
   if y <0: y = 0
   return y

# Default name of plots folder
plotfold='plots'

# Initial parameterization
numcol=6
ymin=0

if len(sys.argv)<2:
   print 'usage: ./canaryCrawler.py [-c or -f] rootdir [-o]'
   quit()

if len(sys.argv)>2:
   ymin = 0
   ylim=10
   root = sys.argv[2]
   plotfold='plots_Specialty'
   if sys.argv[1]=='-f':
     plotfold='plots_Specialty_fft'
     ylim=10000
     ymin=-10000
else:
   ylim=1200
   root = sys.argv[1]

for subdir, dirs, files in os.walk(root):

    # plot each file
    for file in files:

        if str(file)[-4:]=='.csv': 
       
            if plotfold not in os.listdir(subdir):
	       print '** adding plots directory to ',subdir
	       os.mkdir(os.path.join(subdir,plotfold))

            filnam=str(file)[:-4]+'.pdf'
            saveto=os.path.join(subdir,plotfold,filnam)

            # overwrite protection
#            if filnam in os.listdir(os.path.join(subdir,plotfold)) and '-o' not in sys.argv:continue

            print 'plotting '+str(file)+'...'

            # load csv as data frame
            tp=pandas.io.parsers.read_csv(os.path.join(subdir,file), iterator=True, chunksize=1000)
            df = concat(tp, ignore_index=True)
            for i in range(0,len(df.Timestamp)):
                df.Timestamp[i] = datetime.strptime(df.Timestamp[i], '%a %b %d %H:%M:%S %Y')

            # We only want the first 6 cols...
            df = df.ix[:,0:numcol]

            # calibration curve corrections
            for i in range(1,6):
               df.ix[:,i] = df.ix[:,i].map(lambda x: calcurv(x,i))

            # save calibrated csv
            df.to_csv(os.path.join(subdir,plotfold,'calibrated_'+str(file)),sep=',')

            if len(sys.argv)>2:
                df2 = df
                del df
                df=pandas.DataFrame(df2.Timestamp)
                if sys.argv[1]=='-c' or sys.argv[1]=='-f':
                    df['Residence']=df2['P1rms (A)']+df2['P2rms (A)']
                    df['Specialty']=df2['P3rms (A)']+df2['P4rms (A)']
          	    if sys.argv[1]=='-f':
                        df2=pandas.DataFrame(df.Timestamp)

                        df2['Residence']=np.fft.fft(df['Residence'])
		        df2['Specialty']=np.fft.fft(df['Specialty'])
                        df=df2
                        print 'Fourier Transformation Complete'

                        threedee = plt.figure().gca(projection='3d')
                        threedee.scatter(df.index, df['Residence'].real, df['Residence'].imag)
 			threedee.set_xlabel('index')
 			threedee.set_ylabel('real')
 			threedee.set_zlabel('complex')

		        # save in plots directory
   		        filnam=str(file)[:-4]
		        saveto=os.path.join(subdir,plotfold,filnam+'.pdf')
		        print '**** saving plot to ',saveto
                        plt.show()
		        plt.savefig(saveto,dpi=150)
    			continue

            # set up plot
            plt.figure() 
            df.plot(df.Timestamp,alpha=0.6,linewidth=2.3) # add transparency to see overlapping colors
            plt.tight_layout(pad=1.08)
            plt.legend(loc='best') # add legend in non-intrusive location
            plt.legend(loc=5,prop={'size':14}) # 
            plt.ylabel('Current')
            plt.xlabel('Time')
            #plt.gcf().autofmt_xdate(rotation=90)
            plt.xticks(pandas.date_range(df.Timestamp[0],df.Timestamp[len(df.Timestamp)-1],freq='H'))
            plt.gcf().set_size_inches(12.7,9.2)
            plt.gca().set_ylim([ymin,ylim])

            stamp = df.Timestamp[0]
            day = datetime.strftime(stamp,'%a')
            DOM=datetime.strftime(stamp,'%d')
            month =  datetime.strftime(stamp,'%b')
            year =  datetime.strftime(stamp,'%Y')

            plt.title(subdir+'   '+day+' '+month+' '+DOM+' '+year)

            # keep plot

            # save in plots directory
            print '**** saving plot to ',saveto
            plt.savefig(saveto)
plt.close()
