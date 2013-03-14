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
"""pymoult.stack.tools.py
   Published under the GPLv2 license (see LICENSE.txt)

	This modules supplies high level functions for stack manipulaton,
	generating the update functions for the user
"""

from pymoult.stack.utils import *



def safe_redefine(func1,func2,module):
	"""Redefines func1 of moudule as func2 if the code of func1
		cannot be found in the running stack
		func1 and module are string arguments
	"""
	def safe_replace_update(pool,top_frame,bottom_frame):
		if not is_function_in_stack(sys.modules[module].__dict__[func1],top_frame,bottom_frame):
			sys.modules[module].__dict__[func1] = func2
			return True
		else:
			return False
	return safe_replace_update


def reboot_thread(func,*args):
	"""Reboots a thread, statring func with args as the new main function of the thread
	"""
	def reboot_function(pool,top_frame,bottom_frame):
		return continue_with(func,args)
	return reboot_function
