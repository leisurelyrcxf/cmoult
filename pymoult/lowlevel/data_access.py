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

   This module provides the low level tools for accessing data.

   *Classes*
   
   DataAccessor(class,strategy) : creates an iterator over all objects
   of the given class. Strategy is a string describing how objects are
   accessed (immediate,progressive).

   HeapWalker : base class for defining heapwalkers. Has walk_<type>
   methods for each <type> to be walked.

   *Functions for //Update.apply//* 

   traverseHeap(walker,module_names) : walks through the modules of
   given names using the walker given as first argument.

   startLazyUpdate(class,transformer) : sets up the lazy update
   (progressive access, instant update) for all objects of the given
   class. The transformer is a function taking an object as argument.

   startEagerUpdate(class,transformer) : does the eager update
   (immediate access, instant update) for all objects of the given
   class. The transformer is a function taking an object as argument

"""

from queue import Queue
from threading import Lock
import sys
import gc

############################
# Tools for accessing data #
############################

class WrongStrategy(Exception):
    """Error raised if an unknown strategy has been asked"""
    pass

class DataAccessorNull(object):
    """Class for empty objects, used as signal that all targeted data as
    been accessed in the DataAccessor class."""
    pass

class DataAccessor(object):
    """Iteraor that will give access to all instances of a given class,
    using either immediate or progressive strategy"""
    def __init__(self,tclass,strategy="immediate"):
        """Constructor. Takes the class whose instances are to be accessed and
    the strategy to be used as arguments"""
        self.tclass = tclass
        if strategy not in ["immediate","progressive"]:
            raise WrongStrategy()
        self.queue = Queue()
        self.strategy = strategy
        self.accessing = None


    def __iter__(self):
        """Imposed by the Iterator interface. Called when initiating a loop
        over the iterator.
        
        When using the immediate strategy, gets all instances of the
        given class from the pool.

        When using the progressive strategy, used the metaobject
        protocol, binding routers to the __getattribute__ and
        __setattr__ methods of the given class.

        """
        #called when begining an iteration called, we can initiate the getter
        if self.strategy == "immediate":
            pool = gc.get_objects()
            for obj in pool:
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
        
    def __next__(self):
        """Gets the next item of the data accessor. Stops when it meets a
        DataAccessorNull object"""
        item = self.queue.get()
        if type(item) == DataAccessorNull:
            self.accessing = None
            raise StopIteration()
        else:
            self.accessing = item
            return item

    def put(self,item):
        """pushes an item in the data accessor"""
        self.queue.put(item)
        
    def stop(self):
        """pushes a DataAccessorNull object in the data accessor"""
        self.queue.put(DataAccessorNull())
        

class GetItemRouter(object):
    """Router used with the metaobject protocol, as replacement for
    object.__getattribute__, to call a given function whenever a field of
    an object of the given class is read.  The router can also add the
    accessed object to a data accessor.

    """

    def __init__(self,getter=None,dataAccessor=None,function=None):
        """Constructor. Takes a getter, a data accessor instance and a
        function as arguments.
        
        If the getter is set, it will be used instead of object.__getattribute__.
        
        If the dataAccessor is set, whenever a field of an object
        of the given class is read, the object is added to the dataAccessor.

        If the function is set, it will be called every time such read
        action is taken.

        """
        self.dataAccessor = dataAccessor
        self.function = function
        if getter == None:
            self.getter = object.__getattribute__
        else:
            self.getter = getter

    def __call__(self,obj,attr):
        """Handles operations to be donne whenever a field of an object of the
        given class is read."""
        
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
    """Router used with the metaobject protocol, as replacement for
    object.__setattr__, to call a given function whenever a field of an
    object of the given class is written.  The router can also add the
    accessed object to a data accessor.

    """

    def __init__(self,setter=None,dataAccessor=None,function=None):
        """Constructor. Takes a setter, a data accessor instance and a
        function as arguments.
        
        If the setter is set, it will be used instead of object.__setattr__.
        
        If the dataAccessor is set, whenever a field of an object
        of the given class is written, the object is added to the dataAccessor.
        
        If the function is set, it will be called every time such write
        action is taken.
        """
        self.dataAccessor = dataAccessor
        self.function = function
        if setter == None:
            self.setter= object.__setattr__
        else:
            self.setter = setter

    def __call__(self,obj,attr,value):
        """Handles operations to be donne whenever a field of an object of the
        given class is read."""
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
    """Adds a GetItemRouter to a class given as argument. Takes optional
    arguents that will be passed to the GetItemRouter router"""
    router = GetItemRouter(getter=getter,dataAccessor=dataAccessor,function=function)
    tclass.__getattribute__ = lambda o,a : router(o,a)
    tclass.__getterrouter__ = router

def add_setter_router(tclass,setter=None,dataAccessor=None,function=None):
    """Adds a SetItemRouter to a class given as argument. Takes optional
    arguents that will be passed to the SetItemRouter router"""
    router = SetItemRouter(setter=setter,dataAccessor=dataAccessor,function=function)
    tclass.__setattr__ = lambda o,a,v : router(o,a,v)
    tclass.__setterrouter__ = router



############################
# Tools for heap traversal #
############################

class HeapWalker(object):
    """A base class for applying function on elements of the Heap based on
    their type"""

    def walk(self,item):
        methodname = "walk_"+type(item).__name__
        if hasattr(self,methodname):
            self.__getattribute__(methodname)(item)

    def walk_int(self,item):
        pass

    def walk_str(self,item):
        pass

    def walk_module(self,mod):
        for item in dir(mod):
            self.walk(mod[item])

    def walk_object(self,item):
        for attr in dir(item):
            if not (attr.startswith("__") and attr.endswith("__")):
                self.walk(item.__gettattribute__(attr))

                
########################
# Low level mechanisms #
########################

#Update.apply
def traverseHeap(walker,module_names=["__main__"]):
    """Runs the given walker on the globals of the modules names in the
    module_names parameter. If this parameter is empty, it will
    default to the main module.
    """

    if not isinstance(walker,HeapWalker):
        raise TypeError("walker should be of type HeapWalker") 
    modules = [sys.modules[m] for m in filter(lambda x : x in module_names,sys.modules.keys())]
    #For each module of the application, we will run the walker on the globals 
    for modul in modules:
        globs = dir(modul)
        for var in globs:
            if not (var.startswith('__') and var.endswith('__')):
                walker.walk(modul.__getattribute__(var))

#Update.apply
def startLazyUpdate(tclass,transformer):
    """Uses router to set up lazy updates. Takes the target class and the
    transformer function as arguments"""
    add_getter_router(tclass,function=transformer)
    add_setter_router(tclass,function=transformer)
    
#Update.apply
def startEagerUpdate(tclass,transformer):
    """Uses a data accessor to run an eager update. Takes the target class
    and the transformer function as argumments."""
    accessor = DataAccessor(tclass,strategy="immediate")
    for obj in accessor:
        transformer(obj)


