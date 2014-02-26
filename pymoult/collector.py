#    collector.py This file is part of Pymoult
#    Copyright (C) 2013  Sébastien Martinez, Fabien Dagnat, Jérémy Buisson
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

"""pymoult.collector.py
   Published under the GPLv2 license (see LICENSE.txt)

	This module supplies the ObjectPool, used for 
	eager object conversions

"""

import weakref

objectsPool = None

class ObjectsPool(object):
	""" The Pool of objects, keeping a weak reference to all created objects"""
	def __init__(self):
                global objectsPool
                objectsPool = ObjectsPool()
                set_instance_hook(instance_hook)
                self.objects = set()

	def add(self,obj):
		self.objects.add(weakref.ref(obj))

	def cleanup(self):
		d = []
		for ref in self.objects:
			if ref() == None:
				d.append(ref)
		for x in d:
			self.objects.remove(x)

	def pool(self):
		return self.objects


def instance_hook(obj):
	try:
		objectsPool.add(obj)
	except:
		pass

