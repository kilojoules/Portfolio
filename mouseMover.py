#!/usr/local/bin/python
#JULIAN QUICK
#"Daemon" to move mouse slowly, stopping unwanted power save effects
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

mo=PyMouse()

while True:
<<<<<<< HEAD
  time.sleep(.1)
  mo.move(mo.position()[0]+11,mo.position()[1]+11)
=======
  time.sleep(300)
  mo.move(mo.position()[0]+1,mo.position()[1]+1)
>>>>>>> 0970849bfaf5331691ebc30dc29b8b34d3ac49c4
