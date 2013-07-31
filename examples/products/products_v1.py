#!/usr/bin/pypy-dsu

"""products_v1.py
   Published under the GPLv2 license (see LICENSE.txt)
"""

import pymoult
from pymoult.threads import *
from pymoult.updates import *
from pymoult.collector import *
from pymoult.controller import *
from pymoult.stack.generators import *
from pymoult.heap.generators import *
import socket
import time



Socket_port = 5678

class Product(object):
	def __init__(self,name,quantity):
		self.name = name
		self.quantity = quantity


class Site(object):
	def __init__(self,name):
		self.name = name
		self.stock = []
	
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



company = []

def get_site_by_name(name):
	for site in company:
		if site.name == name:
			return site

#Manager active thread

def site_manager_main():
	global company
	for site_name in ["Paris","Lyon","Brest"]:
		site = Site(site_name)
		for product_name in ["apple","banana","cherry","pineapple","mango","lychee"]:
			site.add_product(product_name,5)
		company.append(site) 
	
	while True:
		for site in company:
			s = site.name+" has :"
			for product in site.stock:
				s+=" "+str(product.quantity)+" "+product.name
			print(s)
		
		print("")
		for x in range(10):
			time.sleep(1)



#Socket Passive thread

def order(quantity,product,site):
	the_site = get_site_by_name(site)
	print(the_site.order(product,quantity))

#def move(quantity,product,site):



def do_command(command):
	operands = command.split()
	if operands[0] == "order" and len(operands) == 4:
		order(int(operands[1]),operands[2],operands[3])
	#elif operands[0] == "move" and len(operands) == 4:
	#	move(int(operands[1]),operands[2],operands[3])

def socket_main():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((socket.gethostname(),Socket_port))
	s.listen(5)
	while True:
		conn,addr = s.accept()
		command = conn.recv(9999)
		start_active_update()
		do_command(command)
		start_active_update()
		data = ""
		conn.close()

enable_pool()
manager = DSU_Thread(name="Site_Manager",target=site_manager_main)
socket_thread = DSU_Thread(name="Command_Socket",target=socket_main)
start_controller()
manager.start()
socket_thread.start()


Site_Updater = eager_class_updater(make_global_element("__main__","Site"))
Product_Updater = lazy_class_updater(make_global_element("__main__","Product"))

Command_Updater = safe_redefinition(make_global_element("__main__","do_command"),[make_thread_element(socket_thread)])
Manager_Updater = thread_rebooting(make_thread_element(manager))






