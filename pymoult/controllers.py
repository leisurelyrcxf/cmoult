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

import pymoult.collector
import pymoult.listener
import threading
import sys
from _continuation import continulet
import inspect
import time


Manager = None

def pool_trace(pool,frame,event,arg):
	if event == "call":
		function = frame.f_code
		if function.co_name == "__init__":
			try:
				pool.add(frame.f_locals[function.co_varnames[0]])
			except:
				pass

class RebootException(Exception):
	pass


class Active_Thread(threading.Thread):
	"""This thread uses a trace function to pause itself and run 
		its update function.

		Sleeping_continuation contains either the update continuation or the main
		continuation, depending on what the thread is currently running

		If a pool object is given in the arguments of __init__, the thread will add 
		weak references to every object it creates in the pool.
	"""
	
	def __init__(self,main,pool=None):
		super(Active_Thread,self).__init__()
		self.main = main
		self.pool = pool
		self.sleeping_continuation = None
		self.update_function = None
		self.update_method = None
		self.bottom_frame = None
		self.top_frame = None
		self.trigger_update = None
		self.version = 0
		self.tried_updates = 0
		self.update_time = 0
		self.start_update_time = 0
		self.trace_event = None
		self.trace_arg = None
		self.reboot = False

	def base_trace(self,frame,event,arg):
		self.trace_event = event
		self.trace_arg = arg
		new_trace = None
		if self.update_method != None:
			new_trace = self.update_method(self)
		if self.reboot:
			self.reboot = False
			raise RebootException()
		if new_trace == None:
			return self.trace
		else:
			return new_trace

	def trace(self,frame,event,arg):
		self.top_frame = frame
		if self.trigger_update:
			return self.base_trace(frame,event,arg)
		else:
			if self.pool != None:
				pool_trace(self.pool,frame,event,arg)
			return self.trace

	def run(self):
		self.bottom_frame = inspect.currentframe()
		sys.settrace(self.trace)
		try:
			self.main()
		except RebootException as r:
			#If a Reboot signal has been called, we restart with run
			self.run()


class Passive_Thread(threading.Thread):
	"""This thread uses its start_update method to pause itself and run 
		its update function.

		Sleeping_continuation contains the main continuation. A new continulet is
		created at the beginning of each attempt to update.

		If a pool object is given in the arguments of __init__, the thread will add 
		weak references to every object it creates in the pool.
	"""
	def __init__(self,main,pool=None):
		super(Passive_Thread,self).__init__()
		self.version = 0
		self.tried_updates = 0
		self.update_time = 0
		self.start_update_time = 0
		self.main = main
		self.pool = pool
		self.trigger_update = False
		self.update_function = None
		self.update_method = None
		self.sleeping_continuation = None
		self.bottom_frame = None
		self.top_frame = None

	def trace(self,frame,event,arg):
		if self.pool != None:
			pool_trace(self.pool,frame,event,arg)
		return self.trace

	def run(self):
		self.bottom_frame = inspect.currentframe()
		if self.pool != None:
			sys.settrace(self.trace)
		try:
			self.main()
		except RebootException as r:
			#If a Reboot signal has been called, we restart with run
			self.run()

	def start_update(self):
		if self.update_method != None:
			self.update_method(self)

	


def gen_update(thread):
	def update(continuation):
		updated = thread.update_function(thread.pool,thread.top_frame,thread.bottom_frame)
		continuation.switch(updated)
	return update

def self_update(thread):
	"""Apply update in the current paused thread"""
	if thread.trigger_update and thread.update_function != None:
		thread.top_frame = inspect.currentframe()
		thread.sleeping_continuation = continulet(gen_update(thread))
		if thread.start_update_time == 0:
			thread.start_update_time = time.time()
		thread.trigger_update = not thread.sleeping_continuation.switch()
		thread.tried_updates+=1
		if not thread.trigger_update:
			thread.update_funtion = None
			thread.update_time = time.time() - thread.start_update_time
			thread.start_update_time = 0
			thread.version +=1
	elif thread.update_function == None:
		thread.trigger_update = False


		updated = False
		if self.update_function != None:
			updated = self.update_function(self.pool,self.top_frame,self.bottom_frame)
		continuation.switch(updated)

	def start_update(self):
		if self.trigger_update and self.update_function != None:
			self.top_frame = inspect.currentframe()
			self.sleeping_continuation = continulet(self.update)
			if self.start_update_time == 0:
				t = time.time()
			self.trigger_update = not self.sleeping_continuation.switch()
			self.tried_updates+=1
			if not self.trigger_update:
				self.update_function = None
				self.update_time = time.time() - t
				self.start_update_time = 0
				self.version +=1
		elif self.update_function == None:
			self.trigger_update = False



def start_manager():
	"""Starts the Manager if not already started
	"""
	global Manager
	if Manager == None:
		Manager = pymoult.listener.Listener()
		Manager.start()


def register_threads(threads):
	"""This function adds a reference to all the threads given
		in the argument to the Manager.
	"""
	global Manager
	if Manager != None:
		Manager.controlled_threads+=threads


def enable_eager_object_conversion():
	"""This function creates an new ObjectPool object and returns it"""
	pool = pymoult.collector.ObjectsPool()
	return pool

def start_active_threads(pool=None,*functions):
	"""This function creates active threads for every supplied function and starts them
		an ObjectPool object can be given to be passed to the active threads. 
		Starts the Manager if not already started.
	"""
	start_manager()
	threads = []
	for f in functions:
		t = Active_Thread(f,pool)
		t.start()
		threads.append(t)
	return threads

def start_passive_threads(pool=None,*functions):
	"""This function creates passive threads for every supplied function and starts them
		an ObjectPool object can be given to be passed to the active threads. 
		Starts the Manager if not already started.
	"""
	start_manager()
	threads = []
	for f in functions:
		t = Passive_Thread(f,pool)
		t.start()
		threads.append(t)
	return threads

def start_passive_update():
	"""This function calls the start_update of the current passive thread"""
	thread = threading.current_thread()
	if type(thread) == Passive_Thread:
		thread.start_update()

def set_update_function(function,thread):
	"""This function sets the update function of a given thread"""
	thread.update_function = function

def set_update_method(function,thread):
	"""This function sets the update method of a given thread"""
	thread.update_method = function
