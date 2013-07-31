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
"""pymoult.heap.generators.py
   Published under the GPLv2 license (see LICENSE.txt)
"""

from pymoult.heap.low_level import *
from pymoult.heap.high_level import *
from pymoult.updates import *

def lazy_class_updater(typ):
	class Lazy_Class_Update(Update):
		def __init__(self,new_typ):
			super(Lazy_Class_Update,self).__init__(Element_List([typ]))
			self.set_quiescence_mgmt(quiescent_update=False,guide_quiescence=False,test_quiescence=False)
			self.set_retry_mgmt(retry_fails=False)
			self.pause_to_update = False
			self.new_typ = new_typ 

		def update_function(self):
			start_lazy_update_class(self.area_of_effect[0],self.new_typ)

	return Lazy_Class_Update


def eager_class_updater(typ):
	class Eager_Class_Update(Update):
		def __init__(self,new_typ):
			super(Eager_Class_Update,self).__init__(Element_List([typ]))
			self.set_quiescence_mgmt(quiescent_update=False,guide_quiescence=False,test_quiescence=False)
			self.set_retry_mgmt(retry_fails=False)
			self.pause_to_update = False
			self.new_typ = new_typ 

		def update_function(self):
			eager_class_update(self.area_of_effect[0],self.new_typ)

	return Eager_Class_Update









