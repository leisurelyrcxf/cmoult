#    utils.py This file is part of Pymoult
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
"""pymoult.heap.low_level.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides mid-level functions for heap manipulation
"""


def update_object_to_class(obj,new_class):
	""" convert an object to a new class"""
	#updating methods are automatic when redefining the class	
	
	#setting new class
	obj.__class__ = new_class

	#Converting attributes
	obj.__convert__()
	return True








