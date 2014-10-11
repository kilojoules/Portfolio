#Julian Quick
#Logical flow of functions is from top to bottom
import getInfo
from remove import rem
from delete import delete
from PyQt4 import QtGui, QtCore

#Labes is used to store info for exec commands in textChange function
#bools determines if text has been changed
labes=[]
global bools
global previousnum
global reftex
reftext =': OUT OF BOUNDS'
bools=False

#removes leading descriptior from static lable, appends to signal list
def signalSet(self,name):
   exec('info=str((self.upright.'+name+'.text())).lstrip("'+str(name)+':").strip()')
   return info
#==============================================================================
#When any text box is edited, this function is called
def textChange(self,text,labes,num):
   global bools
   global reftex

   #info about new text is stored in static lable
   if labes[num]=='standard_name':
      try:
          exec('self.upright.'+labes[num]+'.setText(labes[num]+": "+getInfo.getStandardNames()[int(text)])')
      except:
          #exec('self.upright.'+labes[num]+'.setText(labes[num]+": OUT OF BOUNDS")')
          exec('self.upright.'+labes[num]+'.setText(labes[num]+reftex)')
   else:
      exec('self.upright.'+labes[num]+'.setText(labes[num]+": "+text)')
   bools=True
   
   #check standard names
   i=0
   while i<len(dictionary):
      exec('if self.upright.'+dictionary[i]+'.text() == reftex:')
         exec('self.upright.'+dictionary[i]+' = standardNames.index(self.upright.'+dictionary[i]+'.text()')
      

#==============================================================================
#Creates upright hand side lables and text boxes
#upright.lablename is static lable
#upright.edtlablename is text box whch can be edited
def labler(lablename,signalname,self,number):
   #incoming signal names are local, must be global for use in exec
   global selfglobal
   global num
   num=number
   num=number
   selfglobal=self
   #labes array created to refference different values in exec 
   labes.append(str(lablename))
   exec("self.upright."+lablename+'.setText("'+lablename+': '+signalname+'")')
   exec("self.upright."+lablename+".setMinimumSize(self.upright."+lablename+".sizeHint())")
   exec("self.upright."+'edt'+lablename+'.setText(signalname)')
   #Connvects changes in text box to bools logic
   exec('self.upright.edt'+lablename+'.textEdited.connect(lambda: textChange(selfglobal,selfglobal.upright.edt'+lablename+'.text(),labes,'+str(num)+'))')
   exec('textChange(selfglobal,selfglobal.upright.edt'+lablename+'.text(),labes,'+str(num)+')')
   bools=False

def clearRightInfoHub(self,dictionary):
   i=0
   while i<len(dictionary):
      try: 
         exec('self.upright.'+dictionary[i]+'.close()')
         exec('self.upright.edt'+dictionary[i]+'.close()')
      except:
         pass
      i+=1

def makeRightInfoHub(self,headers):
   i=0
   while i<len(headers):
      exec('self.upright.'+headers[i]+'=QtGui.QLabel("'+headers[i]+'",self.upright)')
      exec('self.upright.verticalLayoutScroll.addWidget(self.upright.'+headers[i]+')')
#      exec('self.upright.'+headers[i]+'.move(20,'+str(70*i)+')')
      exec('self.upright.'+'edt'+headers[i]+'=QtGui.QLineEdit(self.upright)')
      exec('self.upright.verticalLayoutScroll.addWidget(self.upright.edt'+headers[i]+')')
 #     exec('self.upright.'+'edt'+headers[i]+'.move(60,'+str(70*i+30)+')')
      exec('self.upright.'+'edt'+headers[i]+'.setFixedWidth(330)')
      i+=1

#==============================================================================
#num is signal's row in varDB.txt
#Bool becomes true when text box(es) are edited
#This function configures button settings based on which radio button is selected
#called by makeSingleRadioButton function (mkbut)
def lookingAt(num,self): #displays metadata based on radiobutton selection
   from addSignal import addsignal
   global previousnum
   global bools
   global reftex
  

   entries=getInfo.getinfo()
   dictionary=getInfo.getDictionary()
   headers=entries[num][0]

   #Check for changes to text boxes with bool
   #num =-1 is a flag that a variable is being deleted, and not to save changes made
   if bools==True and num!=-1:
      bools=False
      reply=QtGui.QMessageBox.question(self, 'Save Changes?', 'Do you want to save these changes?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      if reply==QtGui.QMessageBox.Yes:
        i=1

        #Correct standard name
        for i in self:
          print i
        quit()

        #Get new information from text boxes
        signalist=[[]]
        signalist[0]=[headers[0],signalSet(self,headers[0])]
        while i<len(headers):
          signalist.append([headers[i],signalSet(self,headers[i])])
          i+=1
        #Uses new information to replace previous information
        addsignal(signalist,self,num,{'action':'edit'})
        #lookingAt(num,self)
        return

   #If num is sent as a flag (-1)_, reset it to 0
   #This indicates not to save changes, so bool is set to False
   if num==-1:
      bools=False
      num=0


   #CLEAR RIGHT SIDE INFORMATION HUB
   clearRightInfoHub(self,dictionary)

   #Create framework for upright side information hub
   makeRightInfoHub(self,headers)

#Create new lables and boxes for right side based on button selection
   #Get important info
   i=1
   signals=[]
   while i<len(entries[num][0])+1:
     signals.append(entries[num][i])
#     try:signals.append(entries[num][i])
#     except Exception:pass
     i+=1
   i=0
   #write info to screen
   while i<len(signals):
      labler(entries[num][0][i],signals[i],self,i)
      i+=1
   try: 
      self.deleteButton.clicked.disconnect()
   except Exception: pass
   try: 
      self.saveButton.clicked.disconnect()
   except Exception: pass

   #Update delete button num refference
   self.deleteButton.clicked.connect(lambda: delete(num,self)) 
   
   self.saveButton.clicked.connect(lambda: lookingAt(num,self))
   previousnum=num
   bools=False
