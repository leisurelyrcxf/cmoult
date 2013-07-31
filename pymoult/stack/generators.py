#    generators.py This file is part of Pymoult
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
"""pymoult.stack.generators.py
   Published under the GPLv2 license (see LICENSE.txt)
"""

from pymoult.stack.low_level import *
from pymoult.stack.high_level import *
from pymoult.updates import *
import threading

def safe_redefinition(function,threads):
	l = Element_List(threads)
	d = Element_Dict({"threads":l,"function":function})
	class Safe_Function_Redefinition(Update):
		def __init__(self,new_function):
			super(Safe_Function_Redefinition,self).__init__(d)
			self.set_quiescence_mgmt(quiescent_update=True,guide_quiescence=False,test_quiescence=True)
			self.set_retry_mgmt(retry_fails=True,retry_delay=1,max_retry=3)
			self.pause_to_update = True
			self.new_function = new_function
		
		def test_quiescent_state(self):
			for thread in self.area_of_effect.get_threads():
				if is_function_in_stack(self.area_of_effect["function"],thread):
					return False
			return True

		def test_update_success(self):
			return self.area_of_effect["function"] == self.new_function

		def update_function(self):
			self.area_of_effect["function"] = self.new_function

	return Safe_Function_Redefinition


def thread_rebooting(thread):
	class Thread_Rebooting(Update):
		def __init__(self,new_function,*args):
			super(Thread_Rebooting,self).__init__(Element_List([thread]))
			self.set_quiescence_mgmt(quiescent_update=False,guide_quiescence=False,test_quiescence=False)
			self.set_retry_mgmt(retry_fails=False,retry_delay=0,max_retry=0)
			self.pause_to_update = False
			self.new_function = new_function
			self.args = args

		def update_function(self):
			reboot_thread(self.area_of_effect[0],self.new_function,*self.args)

	return Thread_Rebooting 




