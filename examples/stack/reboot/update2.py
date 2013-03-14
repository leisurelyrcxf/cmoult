#parsed
import sys
import pymoult.controllers
import pymoult.stack.tools
import time

def main3():
	for x in range(4):
		print("This is the 3d version")
		time.sleep(3)
		

myupdate2 = pymoult.stack.tools.reboot_thread(main3)

l = sys.modules["__main__"].threads 
pymoult.controllers.set_update_function(myupdate2,l[0])
