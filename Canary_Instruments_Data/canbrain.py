#!/usr/bin/env python
# Julian Quick
#from sklearn.metrics import accuracy_score
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

# number of seconds for each time snippet
n_DWH = 200
n = 20

maxHeight_DWH = 74.5
maxHeight = 100

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
            tp=pandas.io.parsers.read_csv(os.path.join(subdir,file), iterator=True, chunksize=100)
            print file
            df = concat(tp, ignore_index=True)
            df.Timestamp = df.Timestamp.apply(lambda d: datetime.strptime(d, "%a %b %d %H:%M:%S %Y"))
            # Replace df with simplified Residential/Specialty dataframe
	    df2 = df
            del df
            df=pandas.DataFrame(df2.Timestamp)
	    df['Residence']=df2['P1rms (A)']+df2['P2rms (A)']
            df['Specialty']=df2['P3rms (A)']+df2['P4rms (A)']
            del df2

            # Use arbitraily selected file for accuracy sample
            k+=1
            if k == 5: 
               print "Using data from ",file," for accuracy test. This is not included in the training data."
               sample = (df.Timestamp[n-1:].tolist(),[df['Residence'].iloc[i:i+n].values for i in df.index[:-n+1]], (df['Specialty'] > maxHeight)[n-1:])
               continue

            print "training with ",file

            # record list of arrays of snippets in time
            X.extend([df['Residence'].iloc[i:i+n].values for i in df.index[:-n+1]])

            # record True/False results
            # >72.5 was chosen based on visual insepection
            labels.extend( (df['Specialty'] > maxHeight)[n-1:])

# Make prediction, guage accuracy
'fitting model...'
model.fit(X,labels)
#print "Accuracy is ",accuracy_score(np.array(model.predict(sample[1])),np.array(sample[2]))

def event_detection(day):
   # day is of the form (df.time, df.residential)
   tim = day[0]
   res = day[1]
   pred = model.predict(res)

   P = False
   for i in range(1,len(res)-1):
      if pred[i] == True: #print 'scanning ', pred[i], tim[i-n/2]
         P = True
      if pred[i] == False:
         if P== True: 
	    print "event on ",tim[i-n/2]
 	    P = False
print 'EVENTS'
print '==========='
event_detection((sample[0],sample[1])) 
