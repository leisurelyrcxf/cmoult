#parsed

import sys
import pymoult.controllers
import pymoult.stack.tools

def new_echo2(thread):
	print("This is thread "+str(thread)+" in 3rd version") 


myupdate = pymoult.stack.tools.safe_redefine("echo",new_echo2,"__main__")

threads = sys.modules["__main__"].threads
pymoult.controllers.set_update_function(myupdate,threads[2])
pymoult.controllers.set_update_method(pymoult.controllers.self_update,threads[2])

