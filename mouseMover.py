#!/usr/bin/env python
# JULIAN QUICK
# "Daemon" to move mouse slowly, stopping 
# unwanted power save effects
from pymouse import PyMouse
import time
mo=PyMouse()

while True:
  # Every 300 seconds move the mouse 
  # one pixel down and to the right
  time.sleep(300)
  mo.move(mo.position()[0]+1,mo.position()[1]+1)
