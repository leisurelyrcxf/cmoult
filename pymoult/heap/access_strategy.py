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
    def __init__(self,strategy="immediate",class):
        self.class = class
        if strategy not in ["immediate","progressive"]:
            raise WrongStrategy()
        self.queue = Queue()
        self.strategy = strategy


    def __iter__(self):
        #called when begining an iteration called, we can initiate the getter
        if self.strategy == "immediate":
            for ref in objectsPool.pool():
                obj = ref()
                if isinstance(obj,self.class):
                    self.put(obj)
            self.put(DataAccessorNull())
        if self.strategy == "progressive":
            if type(self.class.__getattribute__) == GetItemRouter:
                self.class.__getattribute__.dataAccessor = self
            else:
                self.class.__gettattribute__ = GetItemRouter(getter = self.class.__gettattribute__,dataAcessor = self)
            if type(self.class.__setattr__) == SetItemRouter:
                self.class.__setattr__.dataAccessor = self
            else:
                self.class.__setattr__ = SetItemRouter(setter = self.class.__setattr__,dataAcessor = self)
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
            self.getter = object.__getitem__
        else:
            self.getter = getter

    def __call__(self,obj,attr):
        if self.dataAccessor != None:
            self.dataAccessor.queue.put(obj)
       
        if self.function != None:
             type(obj).__getattribute__ = self.getter
             self.function(obj)
             type(obj).__getattribute__ = self

        return self.getter(obj,attr)


class SetItemRouter(object):
    def __init__(self,setter=None,dataAccessor=None,function=None):
        self.dataAccessor = dataAccessor
        self.function = function
        if setter == None:
            self.setter = object.__setattr__
        else:
            self.setter = setter

    def __call__(self,obj,attr,value):
        if self.dataAccessor != None:
            self.dataAccessor.queue.put(obj)
       
        if self.function != None:
             type(obj).__setattr__ = self.setter
             self.function(obj)
             type(obj).__setattr__ = self

        return self.setter(obj,attr,value)


#So far, lazy access does not handle heritage 
def setLazyUpdate(class,function):
    if type(class.__getattribute__) == GetItemRouter:
        class.__getattribute__.function = function
    else:
        class.__getattribute__ = GetItemRouter(getter=class.__getattribute__,function=function)
    if type(class.__setattr__) == SetItemRouter:
        class.__setattr__.function = function
    else:
        class.__setattr__ = SetItemRouter(setter=class.__setattr__,function=function)

