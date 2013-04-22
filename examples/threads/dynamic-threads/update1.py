#parsed

import sys
import pymoult.controllers
import pymoult.stack.tools

def new_echo(thread):
	print("This is thread "+str(thread)+" in 2d version") 

myupdate = pymoult.stack.tools.safe_redefine("echo",new_echo,"__main__")

threads = sys.modules["__main__"].threads
pymoult.controllers.set_update_function(myupdate,threads[0])

newthreads = pymoult.controllers.start_active_threads(None,sys.modules["__main__"].genMain(3))
pymoult.controllers.register_threads(newthreads)
threads+=newthreads
