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
from pymoult.highlevel.listener import get_app_listener
from pymoult.highlevel.updates import Update

class BaseManager(object):
    def __init__(self,*threads):
        self.threads=threads
        self.updates = []
        self.current_update = None

    def pause_threads(self):
        self.current_update.pause_hook()
        """suspends all threads managed by the manager"""
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in self.threads:
                suspendThread(t)
        else:
            for t in self.current_update.threads:
                suspendThread(t)

    def resume_threads(self):
        self.current_update.resume_hook()
        """resume the execution of suspended managed threads"""
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in self.threads:
                resumeThread(t)
        else:
            for t in self.current_update.threads:
                resumeThread(t)

    def finish(self):
        """Adds the current update to the list of applied updates and cleans
        up for the next update"""
        listener = get_app_listener()
        listener.add_completed_update(self.current_update.name)
        self.current_update = None

    def postpone(self):
        """Pushes back the current update"""
        self.add_update(self.current_update)
        self.current_update = None
        
    def add_update(self,update):
        self.updates.append(update)
        update.manager = self

    def get_next_update(self):
        self.current_update = self.updates.pop(0)

class Manager(BaseManager):
    def __init__(self,*threads):
        BaseManager.__init__(self,*threads)
        self.current_applied = False
        self.waiting_alterability = False
        self.tried = 0

    def finish(self):
        """Indicates that the update is complete"""
        super(Manager,self).finish()
        self.current_applied = False
        self.waiting_alterability = False
        self.tried = 0

    def postpone(self):
        super(Manager,self).postpone()
        self.current_applied = False
        self.waiting_alterability = False
        self.tried = 0

    def apply_next_update(self):
        if self.current_update is None and len(self.updates) > 0:
            self.get_next_update()
        if self.current_update:
            #If we have not started the update yet, we need to setup
            #for alterabilty
            if not self.waiting_alterability:
                if self.current_update.check_requirements():
                    #Setup before waiting alterability
                    self.current_update.preupdate_setup()
                    self.waiting_alterability = True
                else:
                    #Requirements are not met, we postpone the update 
                    self.postpone()
            #If we are waiting for alterabilty and have not applied
            #the update yet
            if not self.current_applied:
                if self.current_update.check_alterability():
                    self.pause_threads()
                    self.current_update.apply()
                    #Setup before resuming threads
                    self.current_update.preresume_setup()
                    self.resume_threads()
                    self.current_applied = True
                else:
                    self.tried+=1
                    if self.tried >= self.current_applied.max_tries:
                        #We havn't met alterability after
                        #max_tries. We clean everything and postpone the update
                        self.current_update.clean_failed_alterability()
                        self.postpone()
            #if the update has been applied, we wait for it to be over
            if self.current_applied:
                if self.current_update.check_over():
                    self.finish()
            

class ThreadedManager(BaseManager,threading.Thread):
    def __init__(self,*threads):
        """Constructor. Takes threads controlled by the manager in arguments"""
        self.invoked = threading.Event()
        self.current_update_over = threading.Event()
        self.sleepTime=1
        self.stop = False
        BaseManager.__init__(self,*threads)
        threading.Thread.__init__(self)

    def set_sleepTime(self,sleepTime):
        self.sleepTime = sleepTime

    def sleep(self):
        time.sleepTime(self.sleepTime)
        
    def add_update(self,update):
        super(ThreadedManager,self).add_update(update)
        self.invoked.set()
        
    def finish(self):
        """Indicates that the update is complete"""
        super(ThreadedManager,self).finish()
        self.current_update_over.set()
        if len(self.updates) == 0:
            self.invoked.clear()
    
    def wait_current_update(self):
        """Waits for the current update to be complete"""
        self.current_update_over.wait()
        
    def run(self):
        """Life of the manager"""
        while not self.stop:
            #We wait until self.updates is not empty
            self.invoked.wait()
            self.get_next_update()
            #now self.current_update is not None
            if self.current_update.check_requirements():
                #If the requirements are met, we apply the update
                self.current_update_over.clear()
                #Setup before waiting alterability
                self.current_update.preupdate_setup()
                #Wait for alterability
                if self.current_update.wait_alterability():
                    #We have reached the alterability, we suspend the threads and apply
                    self.pause_threads()
                    self.current_update.apply()
                    #Setup before resuming
                    self.current_update.preresume_setup()
                    self.resume_threads()
                    self.current_update.wait_over()
                    #The update is over, we can cleanup and call finish
                    self.current_update.cleanup()
                    self.finish()
                else:
                    #The alterability could not be met, so we postpone
                    #the update after cleaning up
                    self.current_update.clean_failed_alterability()
                    self.postpone()
                    #Wait before sarting over, in case the
                    #current_update is the only one in the list
                    self.sleep()
            else:
                #Else, we add the current update back to list and try again
                self.postpone()
                #Wait before sarting over, in case the current_update is the only one in the list 
                self.sleep()



def generatePreconfiguredManager(managerClass,updateClass,**attributes):
    """Generates a class for a preconfigured Manager, based on a Manager
    class (Threaded or non threaded) and an Update object. The manager
    will always use the mechanisms set up in the update class given to
    it. It is possible to fix some other parameters in the class"""
    if not issubclass(managerClass,BaseManager):
        raise TypeError("First argument must be a BaseManager subclass")
    if not isinstance(update,Update):
        raise TypeError("Second argument must be an Update object")

    class PreconfiguredManager(managerClass):
        """Class for wich updates are bundles for instanciating the bound update class."""
        def __init__(self,*threads):
            super(PreconfiguredManager,self).__init__(self,*threads)
            for attr,value in attributes.iteritems():
                setattr(self,attr,value)

        def add_update(self,bundle):
            """Creates a new update object out of the given bundle. The bundle
            must be a dictionnary that passes arguments to the update
            class __init__ through (compulsory) fields named 'args'
            and 'kwargs' """
            update = updateClass(*bundle['args'],**bundle['kwargs'])
            update.bundle = bundle
            super(PreconfiguredManager,self).add_update(update)
            #Warning : that kind of argument passing works when the
            #update class does not take *args or **kwargs as
            #arguments. If it does, shenanigans may happen
            
