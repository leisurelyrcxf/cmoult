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
	"""Listener class, opening a socket and listening for commands"""
	
        def __init__(self,group=None, target=None, name="Pymoult Listener", verbose=None):
            self.hostname = socket.gethostname()
            self.port = Listener_port 
            self.keep_running = True
            self.update_thread_index = 0
            super(Listener,self).__init__(group=group, target=target, name=name,verbose=verbose)
            self.daemon = True
	
	def start_update(self,update_address):
		if os.path.exists(update_address):
			f = open(update_address,"r")
			if f.readline().strip() == Parsed_header:
				t = imp.find_module(update_address.rstrip(".py"))
				name = os.path.basename(update_address).rstrip(".py")
				def update():
					imp.load_module(name,t[0],t[1],t[2]) 
				update_thread = threading.Thread(target=update,name="update thread "+str(self.update_thread_index))
				update_thread.start()
				self.update_thread_index+=1
			else:
				#Parse the file to get the update function
				print("Error : the update module supplied does not start with " + Parsed_header)
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
                    self.start_update(update_address)
		data = ""
		conn.close()


