#!/usr/bin/env python
# Julian Quick
from sklearn.metrics import accuracy_score
from pandas import *
from datetime import datetime
import numpy as np
import sys
from sklearn.ensemble import RandomForestClassifier
import os

numcol=6
X =[]
labels = []
k = 0
n = 30

if len(sys.argv)<2:
   print 'usage: rootdir'
   quit()

if len(sys.argv)>2:
   root = sys.argv[2]
else:
   root = sys.argv[1]

model = RandomForestClassifier()

# Iterate through each csv file in root
for subdir, dirs, files in os.walk(root):
    for file in files:
        if str(file)[-4:]=='.csv': 
       
            # Parse timestamp
            tp=pandas.io.parsers.read_csv(os.path.join(subdir,file), iterator=True, chunksize=1000)
            df = concat(tp, ignore_index=True)
            for i in range(0,len(df.Timestamp)):
                df.Timestamp[i] = datetime.strptime(df.Timestamp[i], '%a %b %d %H:%M:%S %Y')
	 
            # Replace df with simplified Residential/Specialty dataframe
	    df2 = df
            del df
            df=pandas.DataFrame(df2.Timestamp)
	    df['Residence']=df2['P1rms (A)']+df2['P2rms (A)']
            df['Specialty']=df2['P3rms (A)']+df2['P4rms (A)']
            del df2

            # Use arbitraily selected file for accuracy sample
            k+=1
            if k == 2: 
               print "Using data from ",file," for accuracy test. This is not included in the training data."
               sample = ([df['Residence'].iloc[i:i+n].values for i in df.index[:-n+1]], (df['Specialty'] > 75)[n-1:])
               continue

            print "training with ",file

            # record list of arrays of snippets in time
            X.extend([df['Residence'].iloc[i:i+n].values for i in df.index[:-n+1]])

            # record True/False results
            # >75 was chosen based on visual insepection
            labels.extend( (df['Specialty'] > 75)[n-1:])

# Make prediction, guage accuracy
model.fit(X,labels)
print "Accuracy is ",accuracy_score(np.array(model.predict(sample[0])),np.array(sample[1]))

