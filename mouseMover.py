#!/usr/local/bin/python
#JULIAN QUICK
#"Daemon" to move mouse slowly, stopping unwanted power save effects
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

mo=PyMouse()

while True:
  time.sleep(.1)
  mo.move(mo.position()[0]+11,mo.position()[1]+11)
