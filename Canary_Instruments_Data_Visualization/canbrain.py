#!/usr/bin/env python
# Julian Quick
from pandas import *
from datetime import datetime
import numpy as np
import sys
from sklearn.ensemble import RandomForestClassifier
import os

# Default name of plots folder
plotfold='plots'

# Initial parameterization
numcol=6
ymin=0

if len(sys.argv)<2:
   print 'usage: rootdir'
   quit()

if len(sys.argv)>2:
   root = sys.argv[2]
else:
   root = sys.argv[1]

X =[]
for subdir, dirs, files in os.walk(root):

    # plot each file
    for file in files:

        if str(file)[-4:]=='.csv': 
            print file
       
            tp=pandas.io.parsers.read_csv(os.path.join(subdir,file), iterator=True, chunksize=1000)
            df = concat(tp, ignore_index=True)
            for i in range(0,len(df.Timestamp)):
                df.Timestamp[i] = datetime.strptime(df.Timestamp[i], '%a %b %d %H:%M:%S %Y')
	 
	    df2 = df
            del df
            df=pandas.DataFrame(df2.Timestamp)
	    df['Residence']=df2['P1rms (A)']+df2['P2rms (A)']
            df['Specialty']=df2['P3rms (A)']+df2['P4rms (A)']

            n = 5
            X.extend([df['Residence'].iloc[i:i+n].values for i in df.index[:-n+1]])
            labels = (df['Specialty'] > 0)[n-1:]

model = RandomForestClassifier()
model.fit(X, labels)
model.predict(X)
