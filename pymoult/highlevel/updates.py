#    updates.py This file is part of Pymoult
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

"""pymoult.updates.py
   Published under the GPLv2 license (see LICENSE.txt)

   Provides the Update classes to be used with the managers in the
   managers module.

"""

from pymoult.lowlevel.data_update import *


class UpdateDefinitionError(Exception):
    """Exception raised when using an Update interface"""
    def __init__(self,message):
        super(UpdateDefinitionError,self).__init__()
        self.message = message


class Update(object):
    """Base Update class. Not to be used! For inheritance only!"""
    def __init__(self,manager=None):
        """Constructor. Binds the update to the manager given as argument"""
        self.manager = manager
    
    def setup(self):
        """Configures the manager for the updates"""
        raise UpdateDefinitionError("You should define your own Update-based class")

    def apply(self):
        """Invokes the update in the manager"""
        raise UpdateDefinitionError("You should define your own Update-based class")


class ThreadedUpdate(Update):
    """Update class that works with the ThreadedManager. Not to be used!
    For Inheritance only!"""
    def __init__(self,manager):
        """Constructor"""
        super(ThreadedUpdate,self).__init__(manager=manager)

    def setup(self):
        """Configures the manager for updates"""
        pass
      
    def apply(self):
        """Invokes the update in the manager"""
        self.manager.invoke()

    def wait_update(self):
        """Waits for the update to be complete"""
        self.manager.wait_over() 


class SafeRedefineUpdate(ThreadedUpdate):
    """Update to be used with the SafeRedefineManager"""
    def __init__(self,manager,functions):
        """Constructor. Takes a dictionnary associating old functions to their
        new version in arguelnts"""
        self.functions = functions
        super(SafeRedefineUpdate,self).__init__(manager=manager)

    def setup(self):
        """Sets up the dictionary of functions to be updated in the manager"""
        for function in self.functions.keys():
            self.manager.add_function(function,self.functions[function])
    
class EagerConversionUpdate(Update):
    """Update to be used with the EagerConversionManager"""
    def __init__(self,manager,tcls,cls,transformer):
        """Constructor. Takes the class of the objects to be updated, the new
        class to which they will be udated and a transformer function
        in its arguments

        """
        self.cls=cls
        self.tcls = tcls
        self.transformer = transformer
        super(EagerConversionUpdate,self).__init__(manager=manager)
    
    def setup(self):
        """Sets up the update in the manager"""
        self.manager.cls = self.cls
        self.manager.tcls = self.tcls
        self.manager.transformer = self.transformer

    def apply(self):
        """Invokes the update in the manager"""
        self.manager.run()

    def wait_update(self):
        """waits for the update to be complete"""
        pass


class LazyConversionUpdate(ThreadedUpdate):
    """Update to be used with the LazyConversionManager"""
    def __init__(self,manager,tcls,cls,transformer,ending):
        """Constructor. Takes the class of the objects to be updated, the new
        class to which they will be updated, a transformer and a
        function evaluating the ending condition of the update in its
        arguments.  The ending condition is a function that will
        return True if the ending conditions are met.

        """
        self.cls=cls
        self.tcls=tcls
        self.transformer = transformer
        self.ending = ending
        super(LazyConversionUpdate,self).__init__(manager=manager)

    def setup(self):
        """Sets up the update in the manager"""
        self.manager.cls = self.cls
        self.manager.tcls = self.tcls
        self.manager.transformer = self.transformer
        self.manager.ending = self.ending


class ThreadRebootUpdate(Update):
    """Update to be used with ThreadRebootManager"""
    def __init__(self,manager,units):
        """Constructor.Takes a list of tuples (thread,new main) in its arguments"""
        self.units = units
        super(ThreadRebootUpdate,self).__init__(manager)

    def setup(self):
        """Sets up the update in the manager"""
        for unit in self.units:
            self.manager.units.put(unit)
    
    def apply(self):
        """Invokes the update in the manager"""
        self.manager.run()

    def wait_update(self):
        """Waits for the update to be complete"""
        pass


class HeapTraversalUpdate(Update):
    """Update to be used with HeapTraversalManager"""

    def __init__(self,manager,walker,modules=["__main__"]):
        """Constructor. Takes a heap walker as argument and a list of modules to walk"""
        self.walker = walker
        self.modules = modules
        super(HeapTraversalUpdate,self).__init__(manager)

    def setup(self):
        """Sets up the update in the manager"""
        self.manager.walker = self.walker
        self.manager.modules = self.modules
        

    def apply(self):
        """Invokes the update in the manager"""
        self.manager.run()

    def wait_update(self):
        """Waits for the update to be complete"""
        pass
    
