#    lazy.py This file is part of Pymoult
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
"""pymoult.heap.lazy.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides anything necessary for lazy object updates
"""

import threading
import sys


def lazy_update(typ,conversion):
	"""Redefines the __getattribute__ method of a given class so
		that it will call an update function before acessing the argument

		Keep in mind that, in Python, methods are accessed like attributes 
	"""
	def getattri(self,attr):
		conversion(self)
		return object.__getattribute__(self,attr)

	typ.__getattribute__ = getattri


def make_lazy_update_function(function):
	""" Wraps an update function so that it wont loop endlessly when accessing
		an argument or calling a method 
	"""
	def temp_getattr(obj,attr):
		return object.__getattribute__(obj,attr)

	def update_lazy_function(obj):
		oldtype = type(obj)
		backup_getattr = oldtype.__getattribute__

		oldtype.__getattribute__ = temp_getattr
		
		output = function(obj)

		oldtype.__getattribute__ = backup_getattr
		
		return output
	return update_lazy_function	



