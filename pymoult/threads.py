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

"""pymoult.controllers.py
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
	pass


class DSU_Thread(threading.Thread):
	def __init__(self,group=None, target=None, name=None, args=(), kwargs={}):
		super(DSU_Thread,self).__init__(group=group,name=name,args=args,kwargs=kwargs)
		self.main = target
		self.stoped = False
		self.sleeping_continuation = None
		self.sleeping_continuation_fonction = None
		self.active_update_function = None
                self.active = False
               
	def execute_sleeping_continuation(self,continuation):
		#we switch at once to continue with main
		continuation.switch()
		while not self.stoped:
			if self.sleeping_continuation_fonction != None:
				self.sleeping_continuation_fonction()
			continuation.switch()

	def run(self):
		c = continulet(self.execute_sleeping_continuation)
		c.switch()
		self.sleeping_continuation = c
		while not self.stoped:
			try:
				self.main()
			except RebootException as r:
				#The thread has been rebooted, we just loop again
				pass
	
        def stop(self):
                self.stoped = not self.stoped
                
        def switch(self):
                self.sleeping_continuation.switch()

	def start_update(self):
		if self.active and self.active_update_function != None:
			self.active_update_function()


def start_active_update():
	"""This function calls the start_update of the current active thread"""
	thread = threading.current_thread()
	thread.start_update()

def set_active_update_function(function,thread):
	"""This function sets the active update function of a given thread"""
	thread.active_update_function = function



def get_thread_by_name(name):
        threads = threading.enumerate()
        for thread in threads:
                if thread.name == name:
                        return thread
        return None

def get_current_frames():
        return sys._current_true_frames()


def pause_thread(thread):
        if not hasattr(thread,"pause_event"):
                thread.pause_event = threading.Event()
                thread.pause_event.clear()
                def trace(frame,event,arg):
                        if hasattr(thread,"pause_event"):
                                thread.pause_event.wait()
                        return None
                set_thread_trace(thread,trace)
                               

def resume_thread(thread):
        if hasattr(thread,"pause_event"):
                thread.pause_event.set()
                delattr(thread,"pause_event")

def set_thread_trace(thread,trace):
        sys.settrace_for_thread(thread.ident,trace,True)
