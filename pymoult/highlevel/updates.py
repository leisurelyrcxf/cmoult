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

from pymoult.lowlevel.stack import *
from pymoult.lowlevel.relinking import *
from pymoult.lowlevel.alterability import *
from pymoult.lowlevel.data_access import *
from pymoult.lowlevel.data_update import *
from pymoult.threads import *

class UpdateDefinitionError(Exception):
    """Exception raised when using an Update interface"""
    def __init__(self,message):
        super(UpdateDefinitionError,self).__init__()
        self.message = message


class Update(object):
    def __init__(self,name=None):
        self.applied = False
        self.manager = None
        self.name = name

    def requirements(self):
        raise UpdateDefinitionError("You should define your own Update-based class")
        
    def alterability(self):
        raise UpdateDefinitionError("You should define your own Update-based class")

    def apply(self):
        raise UpdateDefinitionError("You should define your own Update-based class")
    
    def over(self):
        raise UpdateDefinitionError("You should define your own Update-based class")

    
class SafeRedefineUpdate(Update):
    def __init__(self,module,function,new_function):
        self.module = module
        self.function = function
        self.new_function = new_function
        super(SafeRedefineUpdate,self).__init__()

    def requirements(self):
        return True
        
    def alterability(self):
        return not isFunctionInAnyStack(self.function,threads=self.manager.threads)
        

    def apply(self):
        redefineFunction(self.module,self.function,self.new_function)

    def over(self):
        return True
    
class EagerConversionUpdate(Update):
    def __init__(self,cls,new_cls,transformer):
        self.cls = cls
        self.new_cls = new_cls
        self.transformer = transformer
        super(EagerConversionUpdate,self).__init__()

    def object_update(self,obj):
        updateToClass(obj,self.new_cls,self.transformer)
        
    def requirements(self):
        return True

    def alterability(self):
        return True

    def apply(self):
        startEagerUpdate(self.cls,self.object_update)

    def over(self):
        return True


class LazyConversionUpdate(Update):
    def __init__(self,cls,new_cls,transformer):
        self.cls=cls
        self.new_cls=new_cls
        self.transformer = transformer
        super(LazyConversionUpdate,self).__init__()

    def object_update(self,obj):
        updateToClass(obj,self.new_cls,self.transformer)

    def requirements(self):
        return True

    def alterability(self):
        return True

    def apply(self):
        setLazyUpdate(self.cls,self.object_update)

    def over(self):
        return True
        

class ThreadRebootUpdate(Update):
    def __init__(self,thread,new_main,new_args):

        if thread.__class__ is not DSU_Thread and not DSU_Thread in thread.__class__.__bases__:
            raise TypeError("threads in ThreadRebootManager must be of type or of a subtype of DSU_Thread")
        self.thread = thread
        self.new_main = new_main
        self.new_args = new_args
        super(ThreadRebootUpdate,self).__init__()

    def requirements(self):
        return True

    def alterability(self):
        return True
    
    def apply(self):
        resumeThread(self.thread)
        switchMain(self.thread,self.new_main,args=self.new_args)
        resetThread(self.thread)

    def over(self):
        return True


class HeapTraversalUpdate(Update):
    def __init__(self,walker,modules=["__main__"]):
        self.walker = walker
        self.modules = modules
        super(HeapTraversalUpdate,self).__init__()

    def requirements(self):
        return True

    def alterability(self):
        return True

    def apply(self):
        traverseHeap(self.walker,self.modules)
        
    def over(self):
        return True
    
