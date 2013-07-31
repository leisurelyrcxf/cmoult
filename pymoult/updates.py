#    updates.py This file is part of Pymoult
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

"""pymoult.updates.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides the controlled threads and high level
   functions initiating, configuring and starting them.
"""

from pymoult.common.high_level import *
import time
import threading
import sys


class Element(object):
	def __init__(self,getter,setter):
		self.get = getter
		self.set = setter

def make_global_element(module,variable):
	def getter():
		return sys.modules[module].__dict__[variable]
	def setter(value):
		sys.modules[module].__dict__[variable] = value
	e = Element(getter,setter)
	return e

def make_thread_element(thread):
	def getter():
		return thread
	def setter(value):
		raise TypeError("Cannot set a thread")
	e = Element(getter,setter)
	return e


class Element_List(list):
	def __init__(self,elements):
		for elem in elements:
			if not isinstance(elem,Element):
				raise TypeError("can only append Element object")
		super(Element_List,self).__init__(elements)

	def __setitem__(self,key,value):
		element = super(Element_List,self).__getitem__(key)
		element.set(value)

	def __getitem__(self,key):
		element = super(Element_List,self).__getitem__(key)
		return element.get()
	
	def	append(self,element):
		if not isinstance(element,Element):
			raise TypeError("can only append Element object")
		super(Element_List,self).append(element)
	
	def get_threads(self):
		l = []
		for item in self:
			if isinstance(item.get(),threading.Thread):
				l.append(item.get())
		return l


class Element_Dict(dict):
	def __init__(self,elements):
		for key in elements.keys():
			elem = elements[key]
			if not (isinstance(elem,Element) or isinstance(elem,Element_List)):
				raise TypeError("Element_Dict can only contain Elements and Element_List objects")
		super(Element_Dict,self).__init__(elements)
	
	def __setitem__(self,key,value):
		elem = super(Element_Dict,self).__getitem__(key)
		if isinstance(elem,Element):
			elem.set(value)
		else:
			super(Element_Dict,self).__setitem__(key,value)

	def __getitem__(self,key):
		elem = super(Element_Dict,self).__getitem__(key)
		if isinstance(elem,Element): 
			return elem.get()
		else:
			return elem
	
	def change_ref(self,key,value):
		super(Element_Dict,self).__setitem__(key,value)
	
	def get_threads(self):
		l = []
		if self.has_key("threads"):
			for t in self.__getitem__("threads"):
				l.append(t.get())
		return l
		


class Update(object):
	def __init__(self,area_of_effect):
		if not (isinstance(area_of_effect,Element_List) or isinstance(area_of_effect,Element_Dict)):
			raise TypeError("area_of_effect must be an Element_List or Element_Dict object")
		self.area_of_effect = area_of_effect
		self.retry_fails = True
		self.retry_delay = 0
		self.max_retry = 3
		self.pause_to_update = True
		self.quiescent_update = True
		self.guide_quiescence = False
		self.test_quiescence = True

	def pause_threads(self):
		for thread in self.area_of_effect.get_threads():
			pause_thread(thread)

	def resume_threads(self):
		for thread in self.area_of_effect.get_threads():
			resume_thread(thread)

	def set_quiescence_mgmt(self,quiescent_update=True,guide_quiescence=False,test_quiescence=True):
		self.quiescent_update = quiescent_update
		self.guide_quiescence = guide_quiescence
		self.test_quiescence = test_quiescence
	
	def set_retry_mgmt(self,retry_fails=True,retry_delay=0,max_retry=3):
		self.retry_fails=retry_fails
		self.retry_delay=retry_delay
		self.max_retry=max_retry

	def test_quiescent_state(self):
		pass

	def test_update_success(self):
		return True

	def custom_pre(self):
		pass

	def custom_post(self):
		pass

	def update_function(self):
		pass


	def apply(self):
		update_completed = False
		tries = 0
		while not update_completed:
			
			#If quiescent update and test quescient, test it
			if not self.test_quiescence or self.test_quiescent_state():
				
				#Call custom pre hook
				self.custom_pre()
				
				#Pause threads if requested
				if self.pause_to_update:
					self.pause_threads()
				
				#Run the update
				self.update_function()

				#Resume threads if they where paused
				if self.pause_to_update:
					self.resume_threads()

				#Call custom post hook
				self.custom_post()
			
			#If retry_fails is activated, we try again in case of failure
			update_completed = True
			if self.retry_fails:
				if tries < self.max_retry:
					update_completed = self.test_update_success()
					if not update_completed:
						time.sleep(self.retry_delay)




