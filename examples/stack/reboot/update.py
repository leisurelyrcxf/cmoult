#parsed
import sys
import pymoult.controllers
import pymoult.stack.tools
import time

def main2():
	for x in range(4):
		print("This is the 2d version")
		time.sleep(3)
		

myupdate = pymoult.stack.tools.reboot_thread(main2)

l = sys.modules["__main__"].threads 
pymoult.controllers.set_update_function(myupdate,l[0])
pymoult.controllers.set_update_method(pymoult.controllers.self_update,l[0])
