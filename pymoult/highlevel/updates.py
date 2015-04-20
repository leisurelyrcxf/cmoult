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
from pymoult.highlevel.listener import get_app_listener


def isApplied(update):
    listener = get_app_listener()
    return update in listener.applied_updates

class UpdateDefinitionError(Exception):
    """Exception raised when using an Update interface"""
    def __init__(self,message):
        super(UpdateDefinitionError,self).__init__()
        self.message = message


class Update(object):
    def __init__(self,name=None,*threads):
        self.manager = None
        self.name = name
        self.threads = list(threads)

    def check_requirements(self):
        """Function for checking if the requirements for the update are met (must return a bool)"""
        #By default, no requirement is needed
        return True
        
    def preupdate_setup(self):
        """Setup step that happens before waiting for alterability"""
        #By default, no setup needed
        pass
        
    def wait_alterability(self):
        """Function that returns when we are in alterability state. Used in
        threaded managers"""
        raise UpdateDefinitionError("You should define your own Update-based class")

    def check_alterability(self):
        """Function that can be called to check if the alterability criterion
        are met (must return a bool). Used in non threaded managers"""
        raise UpdateDefinitionError("You should define your own Update-based class")

    def apply(self):
        """The actual update step, happens when alterabilty is reached"""
        raise UpdateDefinitionError("You should define your own Update-based class")

    def preresume_setup(self):
        """Setup step that happens after the update was applied, before resuming execution"""
        #By default, no setup needed
        pass
    
    def wait_over(self):
        """function that returns when the update is over. Used in threaded
        managers."""
        #In most cases, the update is finished when apply ends
        pass

    def check_over(self):
        """Function that can be called to check if the update is over (must
        return a bool). Used in non-threaded managers."""
        #In most cases, the update is finished when apply ends
        return True
    

    def cleanup(self):
        """Cleanup step that happens when the update is over"""
        #By default, no cleanup is needed
        pass

    def pause_hook(self):
        """Hook executed when pausing threads"""
        pass

    def resume_hook(self):
        """Hook executed when resume threads"""
        pass


    
class SafeRedefineUpdate(Update):
    def __init__(self,module,function,new_function,name=None):
        self.module = module
        self.function = function
        self.new_function = new_function
        super(SafeRedefineUpdate,self).__init__(name=name)

    def requirements(self):
        return True
        
    def alterability(self):
        return not isFunctionInAnyStack(self.function,threads=self.manager.threads)
        

    def apply(self):
        redefineFunction(self.module,self.function,self.new_function)

    def over(self):
        return True
    
class EagerConversionUpdate(Update):
    def __init__(self,cls,new_cls,transformer,name=None):
        self.cls = cls
        self.new_cls = new_cls
        self.transformer = transformer
        super(EagerConversionUpdate,self).__init__(name=name)

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
    def __init__(self,cls,new_cls,transformer,name=None):
        self.cls=cls
        self.new_cls=new_cls
        self.transformer = transformer
        super(LazyConversionUpdate,self).__init__(name=name)

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
    def __init__(self,thread,new_main,new_args,name=None):

        if thread.__class__ is not DSU_Thread and not DSU_Thread in thread.__class__.__bases__:
            raise TypeError("threads in ThreadRebootManager must be of type or of a subtype of DSU_Thread")
        self.thread = thread
        self.new_main = new_main
        self.new_args = new_args
        super(ThreadRebootUpdate,self).__init__(name=name)

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
    def __init__(self,walker,modules=["__main__"],name=None):
        self.walker = walker
        self.modules = modules
        super(HeapTraversalUpdate,self).__init__(name=name)

    def requirements(self):
        return True

    def alterability(self):
        return True

    def apply(self):
        traverseHeap(self.walker,self.modules)
        
    def over(self):
        return True
    
