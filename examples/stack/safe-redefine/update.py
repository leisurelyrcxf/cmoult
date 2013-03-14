#parsed
import sys
import pymoult.controllers
from pymoult.stack.tools import *

def tst2():
	print "This is the 2d version"

myupdate = safe_redefine("tst1",tst2,"__main__")


l = sys.modules["__main__"].threads 
pymoult.controllers.set_update_function(myupdate,l[0])
