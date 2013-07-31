#    tools.py This file is part of Pymoult
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
"""pymoult.heap.high_level.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides high level heap manipulation functions.
"""

from pymoult.heap.low_level import *
from pymoult.heap.lazy import *
import pymoult.collector 

def start_lazy_update_class(from_class,to_class):
	""" Enables lazy update of objects of the from_class to the to_class
	"""
	def lazy_update_fun(obj):
		if type(obj) == from_class:
			return update_object_to_class(obj,to_class)
	
	lazy_update(from_class,make_lazy_update_function(lazy_update_fun))


def eager_class_update(from_class,to_class):
	""" Starts eager update of objects of the from_class to the to_class
	"""
	result = True
	for ref in pymoult.collector.objectsPool.pool():
		obj = ref()
		if type(obj) == from_class:
			result = result and update_object_to_class(obj,to_class)
	return result



