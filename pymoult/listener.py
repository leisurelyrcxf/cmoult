#    listener.py This file is part of Pymoult
#    Copyright (C) 2013 Sébastien Martinez, Fabien Dagnat, Jérémy Buisson
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
"""pymoult.listener.py
   Published under the GPLv2 license (see LICENSE.txt)

	This module supplies the Listener class and sets global values 
	about the socket server
"""

import threading
import socket
import inspect
from _continuation import continulet
import os
import imp

Listener_port = 4242
Max_recieve = 9999
Trigger_message = "update"
Query_message = "status"
Max_queued_connect = 5
Parsed_header = "#parsed"

class Listener(threading.Thread):
	"""Listener class, opening a socket and listening for commands
		Loads update modules given with the command "update"
	"""
	def __init__(self,group=None, target=None, name=None, verbose=None):
		self.hostname = socket.gethostname()
		self.port = Listener_port 
		self.keep_running = True
		self.trigger_update = False
		self.controlled_threads = []
		super(Listener,self).__init__(group=group, target=target, name=name,verbose=verbose)
		self.daemon = True
	
	def configure_update(self,update_address):
		if os.path.exists(update_address):
			f = open(update_address,"r")
			if f.readline().strip() == Parsed_header:
				t = imp.find_module(update_address.rstrip(".py"))
				name = os.path.basename(update_address).rstrip(".py")
				imp.load_module(name,t[0],t[1],t[2]) 
			else:
				#Parse the file to get the update function
				pass
		else:
			print("Error : the update module supplied was not found")

	def run(self):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.bind((self.hostname,self.port))
		s.listen(Max_queued_connect)
		while self.keep_running:
			conn,addr = s.accept()
			data = conn.recv(Max_recieve)
			if data.strip()[0:len(Trigger_message)] == Trigger_message:
				update_address = data.strip()[len(Trigger_message)+1:]
				self.configure_update(update_address)
				self.trigger_update = True
				for t in self.controlled_threads:
					t.trigger_update = True
			if data.strip()[0:len(Query_message)] == Query_message:
				for thread in self.controlled_threads:
					print("Thread "+str(thread.main.__name__)+" is in version "+str(thread.version))
					print("It has tried "+str(thread.tried_updates)+" times to update ")
					print("It took "+str(thread.update_time)+"s to update this thread")
			

			data = ""
			conn.close()

