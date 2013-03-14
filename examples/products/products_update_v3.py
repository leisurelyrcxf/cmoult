#parsed
"""products_update_v3.py
   Published under the GPLv2 license (see LICENSE.txt)
"""
import pymoult
import pymoult.controllers
import pymoult.stack
import pymoult.stack.tools
import time
import sys



threads = sys.modules["__main__"].threads 
manager_thread = threads[0]

#Function updates
#################


# Manager update
def new_manager_main():
	company = sys.modules["__main__"].company
	while True:
		for site in company:
			s = site.name+" has :"
			for product in site.stock:
				s+=" "+str(product.quantity)+" "+product.name
			s+=" and is marked "+str(site.mark)
			print(s)
		
		print("")
		for x in range(10):
			time.sleep(1)

manager_update_function = pymoult.stack.tools.reboot_thread(new_manager_main)

pymoult.controllers.set_update_function(manager_update_function,manager_thread)


