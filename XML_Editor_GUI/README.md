This is a graphic user interface (GUI) designed to edit an important XML file at the National Center for Atmospheric Research Research Aviation Faucility. 

 File Index 

VDB.py
  program entry point. 
  This is called to initiate the GUI.

VDB.xml
  XML metadata file to be editted

addSignal.py
  XML entry point. This function is called
  with instructions to add, edit, or remove an element.

comboBoxPopUp.py
  This module creates pop-up windows for user comfirmation

delete.py
  Facilitates element delete option. 
  Calls addSignal.py to edit XML
  resets user interface to reflect changes.

getInfo.py
  reads XML document information: variables, categories, standard names

generateButtons.py
  creates display list of variables in XML document. Callse getInfo.py

newSignal.py
  Facilitates adding a new metadata variable. Callse addSignal.py

remove.py
  Facilitates variable delete option. Calls addsignal.py

setup.py/windowSetup.py
  Initializes GUI interface. Creates 3 subdivisions: editor, selection, and menu butons.

standardNaemsCorrection.py
  reads seperate metadata file to generate dropdown menu of standard names
