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

"""pymoult.lowlevel.data_access.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides the low level tools for accessing data

"""
import weakref
from Queue import Queue

class ObjectsPool(object):
	"""A Pool of objects, keeping a weak reference to all created
        objects"""

        objectsPool = None
        @classmethod
        def getObjectsPool(cls):
            p = cls.objectsPool
            if not p:
                raise TypeError("No ObjectsPool was created")
            return cls.objectsPool

	def __init__(self):
            ObjectsPool.objectsPool = self
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


class WrongStrategy(Exception):
    pass

class DataAccessorNull(object):
    pass

class DataAccessor(object):
    def __init__(self,tclass,strategy="immediate"):
        self.tclass = tclass
        if strategy not in ["immediate","progressive"]:
            raise WrongStrategy()
        self.queue = Queue()
        self.strategy = strategy
        self.accessing = None


    def __iter__(self):
        #called when begining an iteration called, we can initiate the getter
        if self.strategy == "immediate":
            for ref in ObjectsPool.getObjectsPool().pool():
                obj = ref()
                if isinstance(obj,self.tclass):
                    self.put(obj)
            self.stop()

        if self.strategy == "progressive":
            if hasattr(self.tclass,"__getterrouter__") and type(self.tclass.__getterrouter__) == GetItemRouter:
                self.tclass.__getterrouter__.dataAccessor = self
            else:
                add_getter_router(self.tclass,getter=self.tclass.__getattribute__,dataAccessor=self)
            if hasattr(self.tclass,"__setterrouter__") and type(self.tclass.__setterrouter__) == SetItemRouter:
                self.tclass.__setterrouter__.dataAccessor = self
            else:
                add_setter_router(self.tclass,setter=self.tclass.__setattr__,dataAccessor = self)
     
        return self
    
    def next(self):
        item = self.queue.get()
        if type(item) == DataAccessorNull:
            self.accessing = None
            raise StopIteration()
        else:
            self.accessing = item
            return item

    def put(self,item):
        self.queue.put(item)
    
    def stop(self):
        self.queue.put(DataAccessorNull())
        

class GetItemRouter(object):
    def __init__(self,getter=None,dataAccessor=None,function=None):
        self.dataAccessor = dataAccessor
        self.function = function
        if getter == None:
            self.getter = object.__getattribute__
        else:
            self.getter = getter

    def __call__(self,obj,attr):
        objtype = type(obj)
        if self.dataAccessor != None and self.dataAccessor.accessing != obj:
              self.dataAccessor.put(obj)
       
        if self.function != None:
            setter_back = None
            getter_back = objtype.__getattribute__
            objtype.__getattribute__ = self.getter
            if hasattr(objtype,"__setterrouter__") and type(objtype.__setterrouter__) == SetItemRouter:
                setter_back = objtype.__setattr__
                objtype.__setattr__ = objtype.__setterrouter__.setter
            self.function(obj)
            if setter_back is not None:
                objtype.__setattr__ = setter_back
            objtype.__getattribute__ = getter_back


        return self.getter(obj,attr)


class SetItemRouter(object):
    def __init__(self,setter=None,dataAccessor=None,function=None):
        self.dataAccessor = dataAccessor
        self.function = function
        if setter == None:
            self.setter= object.__setattr__
        else:
            self.setter = setter

    def __call__(self,obj,attr,value):
        objtype = type(obj)
        if self.dataAccessor != None and self.dataAccessor.accessing != obj:
            self.dataAccessor.queue.put(obj)
       
        if self.function != None:
            getter_back = None
            setter_back = objtype.__setattr__
            objtype.__setattr__ = self.setter
            if hasattr(objtype,"__getterrouter__") and type(objtype.__getterrouter__) == GetItemRouter:
                getter_back = objtype.__getattribute__
                objtype.__getattribute__ = objtype.__getterrouter__.getter
            self.function(obj)
            if getter_back is not None:
                objtype.__getattribute__ = getter_back
            objtype.__setattr__ = setter_back

        return self.setter(obj,attr,value)

def add_getter_router(tclass,getter=None,dataAccessor=None,function=None):
    router = GetItemRouter(getter=getter,dataAccessor=dataAccessor,function=function)
    tclass.__getattribute__ = lambda o,a : router(o,a)
    tclass.__getterrouter__ = router

def add_setter_router(tclass,setter=None,dataAccessor=None,function=None):
    router = SetItemRouter(setter=setter,dataAccessor=dataAccessor,function=function)
    tclass.__setattr__ = lambda o,a,v : router(o,a,v)
    tclass.__setterrouter__ = router

#So far, lazy access does not handle heritage 
def setLazyUpdate(tclass,function):
    add_getter_router(tclass,function=function)
    add_setter_router(tclass,function=function)

def startEagerUpdate(tclass,function):
    accessor = Dataaccessor(tsclass,strategy="immediate")
    for obj in accessor:
        function(obj)
