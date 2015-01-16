#    listener.py This file is part of Pymoult
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
"""pymoult.manager.py
   Published under the GPLv2 license (see LICENSE.txt)
   
   Provides off-the-shelf managers.
"""

import threading
from pymoult.lowlevel.stack import *
from pymoult.lowlevel.relinking import *
from pymoult.lowlevel.alterability import *
from pymoult.lowlevel.data_access import *
from pymoult.lowlevel.data_update import *
from pymoult.threads import *
import time
import Queue

class Manager(object):
    """The base Manager class. Not to be used! For inheritance only""" 
    def __init__(self,sleepTime=3,**units):
        """Constructor. Takes units managed by the manager in arguments"""
        for element in units.keys():
            setattr(self,element,units[element])
        self.invoked = threading.Event()
        self.over = threading.Event()
        self.sleepTime=sleepTime

    def start(self):
        """Starts the manager"""
        pass

    def pause_threads(self):
        """suspends all threads managed by the manager"""
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in self.threads:
                suspendThread(t)

    def resume_threads(self):
        """resume the execution of suspended managed threads"""
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in self.threads:
                resumeThread(t)
        
    def is_alterable(self):
        """Returns True if the application is alterable, False either."""
        return False

    def is_over(self):
        """Returns True if the update is over, False either"""
        return False

    def invoke(self):
        """Invokes the update""" 
        self.invoked.set()

    def finish(self):
        """Indicates that the update is complete"""
        self.over.set()
        self.invoked.clear()
    
    def begin(self):
        """Indicates that the update has begun"""
        self.over.clear()

    def wait_over(self):
        """Waits for the update to be complete"""
        self.over.wait()
    
class ThreadedManager(Manager):
    """Manager using its owwn thread to monitor alterabilty and apply the
       update. No to be used! For inheritance only!"""

    def __init__(self,sleepTime=3,**units):
        """Constructor"""
        self.ownThread = None
        self.stop = False
        super(ThreadedManager,self).__init__(sleepTime=sleepTime,**units)

    def update_function(self):
        """Function handling the update"""
        pass

    def thread_main(self):
        """Main of the manager thread"""
        while not self.stop:
            self.invoked.wait()
            self.begin()
            if self.is_alterable():
                self.update_function()
                while not self.is_over():
                    time.sleep(self.sleepTime)
                self.finish()

    def start(self):
        """Starts the manager"""
        self.ownThread = threading.Thread(target=self.thread_main)
        self.ownThread.start()


class SafeRedefineManager(ThreadedManager):
    """Manager for handling safe redefinition update.  Its alretability
    criterion is "the function to be updated is not in the stack of
    the managed threads. Uses function redefinition from lowlevel.relinking module.
    """

    def __init__(self,threads,sleepTime=3):
        """Constructor"""
        self.functions = Queue.Queue()
        super(SafeRedefineManager,self).__init__(sleepTime=sleepTime,threads=threads)

    def is_alterable(self,function):
        """Alterability criterion : the given function is not in the stack of
        the managed threads"""
        for thread in self.threads:
            if isFunctionInStack(function,thread):
                return False
        return True
  
    def add_function(self,module,function,new_function):
        """Adds a pair (old function, new function) to the queue of functions
        to be redefined"""
        self.functions.put((module,function,new_function))

    def thread_main(self):
        """Main of the manager thread"""
        while not self.stop:
            self.invoked.wait()
            self.begin()
            while True:
                try:
                    function = self.functions.get(False)
                except Queue.Empty:
                    self.finish()
                    break
                function_updated = False
                while not function_updated:
                    if self.is_alterable(function[1]):
                        self.pause_threads()
                        redefineFunction(function[0],function[1],function[2])
                        function_updated = True
                        self.resume_threads()
                    time.sleep(self.sleepTime)
     

                        
class EagerConversionManager(Manager):
    """Uses Eager conversion to update objects of a given class. Combines
    immediate access strategy and on-demand conversion moment.
    Updates objects to a new given class, applies a transformer on it
    if specified. Does not have alterability criteria.

    """ 

    def __init__(self,threads=[],sleepTime=3):
        """Constructor"""
        self.cls = None
        self.tcls = None
        self.transformer = None
        super(EagerConversionManager,self).__init__(threads=threads,sleepTime=sleepTime)
    
    def start(self):
        """Starts the manager. Creates the ObjectsPool if does not exist"""
        try:
            ObjectsPool.getObjectsPool()
        except TypeError:
            ObjectsPool()

    def run(self):
        """Handles the eager update of objects""" 
        if self.cls:
            def t(obj):
                updateToClass(obj,self.cls,transformer = self.transformer)
            self.pause_threads()
            if self.tcls:
                startEagerUpdate(self.tcls,t)
            self.resume_threads()


class LazyConversionManager(ThreadedManager):
    """Uses Lazy conversion to updates objects of a given class. Combines
    progressive access strategy and on-need conversion moment. Updates
    objects to a new given class, applies a transformer on it if
    specified. Does not have alterability criteria.

    """
    def __init__(self,sleepTime=3):
        """Constructor"""
        self.cls = None
        self.tcls = None
        self.transformer = None
        self.ending =None
        super(LazyConversionManager,self).__init__(sleepTime=sleepTime)
        
    def thread_main(self):
        """Main of the manager thread"""
        while not self.stop:
            self.invoked.wait()
            if self.cls:
                def t(obj):
                    updateToClass(obj,self.cls,transformer = self.transformer)
                self.begin()
                if self.tcls:
                    setLazyUpdate(self.tcls,t)
                if self.ending:
                    while not self.ending():
                        time.sleep(self.sleepTime)
                self.finish()
        
        
class ThreadRebootManager(Manager):
    """Updates the main of threads and reboots them. Does not have
    alterability criteria"""
    def __init__(self):
        """Constructor"""
        self.units = Queue.Queue()
        super(ThreadRebootManager,self).__init__()

    def run(self):
        """Handles main switching and rebooting of threads"""
        reboot_list = []
        while True:
            try:
                unit = self.units.get(False)
            except Queue.Empty:
                break
            thread = unit[0] #Thread to be rebooted
            main = unit[1] #new main function
            args = unit[2] #new args
            if thread.__class__ is not DSU_Thread and not DSU_Thread in thread.__class__.__bases__:
                raise TypeError("threads in ThreadRebootManager must be of type or of a subtype of DSU_Thread")
            switchMain(thread,main,args=args)
            reboot_list.append(thread)
        for thread in reboot_list:
            resetThread(thread)
                
                
class HeapTraversalManager(Manager):
    """Traverses the heap with the walker given by the update. Pauses the
    application when doing so"""
    
    def __init__(self,threads):
        """Constructor"""
        self.walker = None
        self.modules = []
        super(HeapTraversalManager,self).__init__(threads=threads)
    
    def run(self):
        """Walks the heap while the application is suspended"""
        if self.walker and len(self.modules) > 0:
            self.pause_threads()
            traverseHeap(self.walker,self.modules)
            self.resume_threads()



        
        

