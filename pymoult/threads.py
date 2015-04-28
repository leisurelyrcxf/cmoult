#    controllers.py This file is part of Pymoult
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

"""pymoult.threads.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides the controlled threads and high level
   functions initiating, configuring and starting them.
"""

import threading
import sys
from _continuation import continulet
import inspect
import time


class RebootException(Exception):
    """Exception raised for rebooting a thread"""
    pass


class DSU_Thread(threading.Thread):
    """Thread enhanced with DSU features:
    
    - The thread can be rebooted by raising a RebootException
    - The thread can switch to continuation if requested
    """
    def __init__(self,active=False,group=None, target=None, name=None, args=(), kwargs={}):
        """Constructor. Takes classic thread arguments"""
        super(DSU_Thread,self).__init__(group=group,name=name,args=args,kwargs=kwargs)
        self.__main = target
        self.keep_running = True
        self.sleeping_continuation = None
        self.sleeping_continuation_function = None
        self.active_update_function = None
        self.active = active
        self.last_update_point = None
               
    def set_active(self):
        self.active = True

    def set_passive(self):
        self.active = False

    def execute_sleeping_continuation(self,continuation):
        """Switches to the continuation associated with the thread. If
        sleeping_continuation_function is set, calls it.  Called once
        when bootstraping the thread
        """
        #we switch at once to continue with main
        continuation.switch()
        while True:
            if self.sleeping_continuation_function != None:
                self.sleeping_continuation_function()
            continuation.switch()

    def run(self):
        """Bootstraps the thread"""
        c = continulet(self.execute_sleeping_continuation)
        c.switch()
        self.sleeping_continuation = c
        while self.keep_running:
            self.toogle_loop_main()
            try:
                self.main()
            except RebootException as r:
                #The thread has been rebooted, we just loop again
                pass
	
    def toogle_loop_main(self):
        """Turns on restarting the main function when it finishes (disabled by
        default)"""
        self.keep_running = not self.keep_running

    def switch(self):
        """Switch to the sleeping continuation"""
        self.sleeping_continuation.switch()

    def start_update(self):
        """Starts active update. If the active is set (active update mode),
        the thread will run the udate function set in
        active_update_function"""
        if self.active:
            if self.active_update_function is not None:
                self.active_update_function()
                self.active_update_function = None
        else:
            if hasattr(self,"static_point_event"):
                self.static_point_event.set()
                if hasattr(self,"pause_event"):
                    self.pause_event.wait()

    def main(self):
        if self.__main:
            self.__main()
                
                
def set_active_update_function(function,thread):
    """This function sets the active update function of a given thread"""
    thread.active_update_function = function

def get_thread_by_name(name):
    """returns the thread whose name is given as argument. Returns None if
    no thread as such name"""
    threads = threading.enumerate()
    for thread in threads:
        if thread.name == name:
            return thread
    return None

def set_thread_trace(thread,trace):
    """Sets the given trace to the given thread. Starts the trace
    immediately (does not wait forthe next function return)"""
    sys.settrace_for_thread(thread.ident,trace,True)




