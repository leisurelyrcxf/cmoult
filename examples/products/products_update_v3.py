#parsed
"""products_update_v3.py
   Published under the GPLv2 license (see LICENSE.txt)
"""
from pymoult.stack.high_level import *
from pymoult.common.high_level import *
import time
import sys




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

manager_update_v3 = sys.modules["__main__"].Manager_Updater(new_manager_main)
manager_update_v3.apply()
