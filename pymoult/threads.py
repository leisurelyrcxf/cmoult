#    threads.py This file is part of Pymoult
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
import inspect
import time
from pymoult.highlevel.listener import log


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
        self.active_update_function = None
        self.active = active
        self.last_update_point = None
               
    def set_active(self):
        self.active = True

    def set_passive(self):
        self.active = False

    def run(self):
        """Bootstraps the thread"""
        while self.keep_running:
            self.keep_running = False
            try:
                self.main()
            except RebootException as r:
                #The thread has been rebooted, we just loop again
                pass

    def allow_reboot(self):
        """Activates thread rebooting until next reboot"""
        self.keep_running = True

    def start_update(self):
        """Starts active update. If the active is set (active update mode),
        the thread will run the udate function set in
        active_update_function"""
        if self.active:
            if self.active_update_function is not None:
                self.active_update_function()
                self.active_update_function = None
        else:
            if hasattr(self, "static_point_event"):
                self.static_point_event.set()
                if hasattr(self, "static_wait"):
                    try:
                        self.suspend()
                    except ThreadError as e:
                        log(1,"At static point, thread "+str(self.name)+" met a ThreadError when suspending : "+str(e))
                    delattr(self, "static_wait")
                    
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
    try:
        sys.settrace_for_thread(thread.ident,trace,True)
    except ThreadError as e:
        log(1,"setting trace "+trace.__name__+" on thread "+str(thread.name)+" met a ThreadError : "+str(e))
        

