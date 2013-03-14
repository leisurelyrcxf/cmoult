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
"""pymoult.stack.utils.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module supplied mid-level functions for stack manipulation
"""

import sys
import threading
import pymoult.controllers
import inspect
from _continuation import continulet

def is_function_in_stack(func,top_frame,bottom_frame):
	"""Seeks for func code in the stack"""
	x = top_frame
	while x is not bottom_frame:
		if x.f_code is func.func_code:
			return True
		x = x.f_back
	return False


def replace_function(func1,func2):
	"""replaces func1 by func2 in module"""
	func1 = func2

def continue_with(func,args=None):
	def m():
		return func(*args)
	"""Continues the thread with the given function and arguments"""
	thread = threading.current_thread()
	thread.reboot = True
	if type(thread) == pymoult.controllers.Active_Thread:
		thread.main = m
	elif type(thread) == pymoult.controllers.Passive_Thread:
		thread.main = m
	else:
			return False
	return True






