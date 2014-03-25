#    access_strategy.py This file is part of Pymoult
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
"""pymoult.heap.access_startegy.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides strategy to acess the data in the heap.
"""

from pymoult.collector import objectsPool
from Queue import Queue


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


    def __iter__(self):
        #called when begining an iteration called, we can initiate the getter
        if self.strategy == "immediate":
            for ref in objectsPool.pool():
                obj = ref()
                if isinstance(obj,self.tclass):
                    self.put(obj)
            self.put(DataAccessorNull())
        if self.strategy == "progressive":
            if type(self.tclass.__getattribute__) == GetItemRouter:
                self.tclass.__getattribute__.dataAccessor = self
            else:
                self.tclass.__gettattribute__ = GetItemRouter(getter = self.tclass.__gettattribute__,dataAcessor = self)
            if type(self.tclass.__setattr__) == SetItemRouter:
                self.tclass.__setattr__.dataAccessor = self
            else:
                self.tclass.__setattr__ = SetItemRouter(setter = self.tclass.__setattr__,dataAcessor = self)
                return self
    
    def next(self):
        item = self.queue.get()
        if type(item) == DataAccessorNull:
            raise StopIteration()
        else:
            return item

    def put(self,item):
        self.queue.put(item)
        
        

class GetItemRouter(object):
    def __init__(self,getter=None,dataAccessor=None,function=None):
        self.dataAccessor = dataAccessor
        self.function = function
        if getter == None:
            self.getter = object.__getattribute__
        else:
            self.getter = getter

    def __call__(self,obj,attr):
        if self.dataAccessor != None:
            self.dataAccessor.queue.put(obj)
       
        if self.function != None:
            setter_back = None
            getter_back = type(obj).__getattribute__
            type(obj).__getattribute__ = self.getter
            if hasattr(type(obj),"__setterrouter__")and type(type(obj).__setterrouter__) == SetItemRouter:
                setter_back = type(obj).__setattr__
                type(obj).__setattr__ = type(obj).__setterrouter__.setter
            self.function(obj)
            if setter_back is not None:
                type(obj).__setattr__ = setter_back
            type(obj).__getattribute__ = getter_back


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
        if self.dataAccessor != None:
            self.dataAccessor.queue.put(obj)
       
        if self.function != None:
            getter_back = None
            setter_back = type(obj).__setattr__
            type(obj).__setattr__ = self.setter
            if hasattr(type(obj),"__getterrouter__") and type(type(obj).__getterrouter__) == GetItemRouter:
                getter_back = type(obj).__getattribute__
                type(obj).__getattribute__ = type(obj).__getterrouter__.getter
            self.function(obj)
            if getter_back is not None:
                type(obj).__getattribute__ = getter_back
            type(obj).__setattr__ = setter_back

        return self.setter(obj,attr,value)

def add_getter_router(tclass,getter=None,dataAccessor=None,function=None):
    router = GetItemRouter(getter=getter,dataAccessor=dataAccessor,function=function)
    tclass.__getattribute__ = lambda o,a : router(o,a)
    tclass.__getterrouter__ = router

def add_setter_touter(tclass,setter=None,dataAccessor=None,function=None):
    router = SetItemRouter(setter=setter,dataAccessor=dataAccessor,function=function)
    tclass.__setattr__ = lambda o,a,v : router(o,a,v)
    tclass.__setterrouter__ = router

#So far, lazy access does not handle heritage 
def setLazyUpdate(tclass,function):
    add_getter_router(tclass,function=function)
    add_setter_touter(tclass,function=function)

