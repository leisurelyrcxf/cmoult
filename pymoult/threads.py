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


Manager = None


class RebootException(Exception):
	pass


class DSU_Thread(threading.Thread):
	def __init__(self,group=None, target=None, name=None, args=(), kwargs={}):
		super(DSU_Thread,self).__init__(group=group,name=name,args=args,kwargs=kwargs)
		self.main = target
		self.stop = False
		self.sleeping_continuation = None
		self.sleeping_continuation_fonction = None
		self.active = False
		self.active_update_function = None

	def set_passive(self):
		self.active = False

	def set_active(self):
		self.active = True

	def execute_sleeping_continuation(self,continuation):
		#we switch at once to continue with main
		continuation.switch()
		while not self.stop:
			if self.sleeping_continuation_fonction != None:
				self.sleeping_continuation_fonction()
			continuation.switch()

	def run(self):
		c = continulet(self.execute_sleeping_continuation)
		c.switch()
		self.sleeping_continuation = c
		while not self.stop:
			try:
				self.main()
			except RebootException as r:
				#The thread has been rebooted, we just loop again
				pass
	
	def start_update(self):
		if self.active and self.active_update_function != None:
			self.active_update_function()


def start_passive_update():
	"""This function calls the start_update of the current active thread"""
	thread = threading.current_thread()
	thread.start_update()

def set_active_update_function(function,thread):
	"""This function sets the active update function of a given thread"""
	thread.active_update_function = function



