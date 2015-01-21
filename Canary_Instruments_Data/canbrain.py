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
X_DWH =[]
X_Range =[]
labels_DWH = []
labels_Range = []
k = 0

# number of seconds for each time snippet
n_DWH = 200
n_Range = 20

# min height to be considered an event
maxHeight_DWH = 74.5
maxHeight_Range = 100

# mac adress samples
samples_DWH = {}
samples_Range = {}

# Check arguments
if len(sys.argv)<2:
   print 'usage: rootdir'
   quit()

if len(sys.argv)>2:
   root = sys.argv[2]
else:
   root = sys.argv[1]

# Initialize Random Forest Model
model = {}
model['DWH'] = RandomForestClassifier()
model['Range'] = RandomForestClassifier()

# Iterate through each csv file in root
for subdir, dirs, files in os.walk(root):
    for file in files:
        if str(file)[-4:]=='.csv': 

            # Record mac adress
            print subdir
            mac_adress = subdir.split(os.sep)[1]
            if mac_adress not in samples_DWH and 'DWH' in mac_adress: 
               samples_DWH[mac_adress] = []
               k = 0
            if mac_adress not in samples_Range and 'Range' in mac_adress: 
               samples_Range[mac_adress] = []
               k = 0
       
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
            if k >= 5 and k <=13: 
               print "Using data from ",file," for accuracy test. This is not included in the training data."
               if 'DWH' in mac_adress:
                  samples_DWH[mac_adress] += (df.Timestamp[n_DWH-1:].tolist(),[df['Residence'].iloc[i:i+n_DWH].values for i in df.index[:-n_DWH+1]], (df['Specialty'] > maxHeight_DWH)[n_DWH-1:])

               if 'Range' in mac_adress:
                  samples_Range[mac_adress] = (df.Timestamp[n_Range-1:].tolist(),[df['Residence'].iloc[i:i+n_Range].values for i in df.index[:-n_Range+1]], (df['Specialty'] > maxHeight_Range)[n_Range-1:])
               continue

            print "training with ",file,'   ' ,mac_adress

            # record list of arrays of snippets in time
            if 'Range' in mac_adress:
                X_Range.extend([df['Residence'].iloc[i:i+n_Range].values for i in df.index[:-n_Range+1]])
                labels_Range.extend( (df['Specialty'] > maxHeight_Range)[n_Range-1:])
            if 'DWH' in mac_adress:
                X_DWH.extend([df['Residence'].iloc[i:i+n_DWH].values for i in df.index[:-n_DWH+1]])
                labels_DWH.extend( (df['Specialty'] > maxHeight_DWH)[n_DWH-1:])

            # record True/False results
            # >72.5 was chosen based on visual insepection

# Make prediction, guage accuracy
'fitting model...'
if X_Range: model['Range'].fit(X_Range,labels_Range)
if X_DWH: model['DWH'].fit(X_DWH,labels_DWH)
#print "Accuracy is ",accuracy_score(np.array(model.predict(sample[1])),np.array(sample[2]))

def event_detection(day,ident,event):
   # day is of the form (df.time, df.residential)
   tim = day[0]
   res = day[1]
   pred = model[event].predict(res)

   P = False
   for i in range(1,len(res)-1):
      if pred[i] == True: #print 'scanning ', pred[i], tim[i-n/2]
         P = True
      if pred[i] == False:
         if P== True: 
	    print ident,": event on ",tim[i],'  ',event
 	    P = False
print 'EVENTS'
print '==========='
for key in samples_DWH:
   event_detection((samples_DWH[key][0],samples_DWH[key][1]),key,'DWH')

for key in samples_Range:
   event_detection((samples_Range[key][0],samples_Range[key][1]),key,'Range')
