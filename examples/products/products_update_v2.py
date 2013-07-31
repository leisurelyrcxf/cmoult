#parsed
"""products_update_v2.py
   Published under the GPLv2 license (see LICENSE.txt)
"""
from pymoult.stack.high_level import *
from pymoult.heap.high_level import *
from pymoult.common.high_level import *
import time
import sys
import threading

manager_thread = get_thread_by_name("Site_Manager")
socket_thread = get_thread_by_name("Command_Socket")


#Object updates
###############

# Product updates
class ProductV2(object):
	def __init__(self,name,quantity):
		self.name = name
		self.quantity = quantity
		self.mark = 0
		self.votes = 0
	
	def __convert__(self):
		self.mark = 0
		self.votes = 0
	
	def give_mark(self,mark):
		if self.votes == 0:
			self.mark = mark
			self.votes = 1
		else:
			self.mark = self.votes*(self.mark + mark) / float((self.votes*( self.votes +1) ))
			self.votes +=1

product_update_v2 = sys.modules["__main__"].Product_Updater(ProductV2)
product_update_v2.apply()

# Site updates

class SiteV2(object):
	def __init__(self,name):
		self.name = name
		self.stock = []
		self.mark = 0
	
	def __convert__(self):
		self.mark = 0
	
	def order(self,product,quantity):
		the_product = self.get_product(product)
		if the_product != None:
				if the_product.quantity >= quantity:
					the_product.quantity -= quantity
					return str(quantity)+" "+product+" were ordered from "+self.name
				else:
					return "There is not enough "+product+" in "+self.name
		else:
			return "There is no "+product+" in site "+self.name
	
	def get_product(self,product):
		for the_product in self.stock:
			if the_product.name == product:
				return the_product
		return None


	def add_product(self,product,quantity):
		the_product = self.get_product(product)
		if the_product != None:
			the_product.quantity+=quantity
		else:
			self.stock.append(Product(product,quantity))

	def mark_product(self,product,mark):
		the_product = self.get_product(product)
		if the_product != None:
			the_product.give_mark(mark)
			self.update_mark()
			return " The product "+product+" has been marked, its new mark is "+str(the_product.mark)
		else:
			return "There is no "+product+" in site "+self.name

	def update_mark(self):
		n = len(self.stock)
		m = 0
		for product in self.stock:
			m += product.mark
		self.mark = float(m) / float(n)

site_update_v2 = sys.modules["__main__"].Site_Updater(SiteV2)
site_update_v2.apply()

#Function updates
#################


# Manager update

#No update for the functions of the manager

# Socket update


def rate(mark,product,site):
	the_site = sys.modules["__main__"].get_site_by_name(site)
	print(the_site.mark_product(product,mark))


def new_do_command(command):
	operands = command.split()
	if operands[0] == "order" and len(operands) == 4:
		sys.modules["__main__"].order(int(operands[1]),operands[2],operands[3])
	if operands[0] == "rate" and len(operands) == 4:
		rate(float(operands[1]),operands[2],operands[3])

command_update_v2 = sys.modules["__main__"].Command_Updater(new_do_command) 
command_update_v2.apply()
