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

   This module supplies the Listener class that opens a socket server,
   listening to commands from the user, enabling the submission of
   updates.  The socket is bound to the local hostname (given by
   socket.gethostname()) and to the 4242 port.

   Updates supplied through an instance of Listener are run in their
   own thread. They are supplied by sending the command "update
   <python file>" to the listener. The code of updates must begin with
   "#parsed"

"""

import threading
import socket
import inspect
from _continuation import continulet
import os
import imp

Listener_port = 4242
Max_recieve = 9999
Invoke_message = "update"
Max_queued_connect = 5
Parsed_header = "#parsed"


app_listener = None

def get_app_listener():
    return app_listener


class Listener(threading.Thread):
    """Opens a socket server for users to supply updates."""
    
    def __init__(self,group=None, target=None, name="Pymoult Listener", verbose=None):
        """Constructor using the same parameters as a regular thread object"""
        global app_listener 
        self.hostname = socket.gethostname()
        self.port = Listener_port 
        self.keep_running = True
        self.update_thread_index = 0
        super(Listener,self).__init__(group=group, target=target, name=name,verbose=verbose)
        self.daemon = True
        self.applied_updates = []
        app_listener = self

    def add_completed_update(self,update):
        self.applied_updates.append(update)
        
    def start_update(self,update_address):
        """Load the update code and runs it in a new thread"""
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
        """Main loop of the thread, opens the socket and parses the commands"""
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.hostname,self.port))
        s.listen(Max_queued_connect)
        while self.keep_running:
            conn,addr = s.accept()
            data = conn.recv(Max_recieve)
            if data.strip()[0:len(Invoke_message)] == Invoke_message:
                update_address = data.strip()[len(Invoke_message)+1:]
                self.start_update(update_address)
                data = ""
                conn.close()


