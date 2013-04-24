#parsed

import sys
import pymoult.controllers
import pymoult.stack.tools
import time


def travel4(a,b):
	a.release()
	time.sleep(8)
	b.acquire()

def travel5(a,b):
	a.release()
	time.sleep(5)
	b.acquire()

def travel6(a,b):
	a.release()
	time.sleep(9)
	b.acquire()


myupdate1 = pymoult.stack.tools.safe_redefine("travel1",travel4,"__main__")
myupdate2 = pymoult.stack.tools.safe_redefine("travel2",travel5,"__main__")
myupdate3 = pymoult.stack.tools.safe_redefine("travel3",travel6,"__main__")

l = sys.modules["__main__"].threads
pymoult.controllers.set_update_function(myupdate1,l[0])
pymoult.controllers.set_update_function(myupdate2,l[1])
pymoult.controllers.set_update_function(myupdate3,l[2])
pymoult.controllers.set_update_method(pymoult.controllers.self_update,l[0])
pymoult.controllers.set_update_method(pymoult.controllers.self_update,l[1])
pymoult.controllers.set_update_method(pymoult.controllers.self_update,l[2])
