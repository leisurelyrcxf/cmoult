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

class Manager(object):
    def __init__(self,*threads):
        self.threads=threads
        self.updates = []
        self.current_update = None

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

    def add_update(self,update):
        self.updates.append(update)
        update.manager = self

    def apply_next_update(self):
        if self.current_update is None and len(self.updates) > 0:
            self.current_update = self.updates.pop(0)
        if self.current_update:
            if not self.current_update.applied:
                if self.current_update.requirements() and self.current_update.alterability():
                #requirements will be given in alterability
                        self.pause_threads()
                        self.current_update.apply()
                        self.resume_threads()
                        self.current_update.applied = True
                if self.current_update.applied:
                    if self.current_update.over():
                        listener = get_app_listener()
                        listener.add_completed_update(self.current_update.name)
                        self.current_update = None
            


class ThreadedManager(Manager,threading.Thread):
    def __init__(self,*threads):
        """Constructor. Takes threads controlled by the manager in arguments"""
        self.invoked = threading.Event()
        self.over = threading.Event()
        self.sleepTime=1
        self.stop = False
        Manager.__init__(self,*threads)
        threading.Thread.__init__(self)

    def set_sleepTime(self,sleepTime):
        self.sleepTime = sleepTime
        
    def add_update(self,update):
        super(ThreadedManager,self).add_update(update)
        self.invoked.set()
        
    def finish(self):
        """Indicates that the update is complete"""
        self.over.set()
        if len(self.updates) == 0:
            self.invoked.clear()
    
    def wait(self):
        """Waits for the update to be complete"""
        self.over.wait()
        
    def run(self):
        """Life of the manager"""
        while not self.stop:
            self.invoked.wait()
            time.sleep(self.sleepTime)
            if self.current_update == None:
                self.current_update = self.updates.pop(0)
            self.over.clear()
            if not self.current_update.applied:
                if self.current_update.requirements() and self.current_update.alterability():
                    self.pause_threads()
                    self.current_update.apply()
                    self.resume_threads()
                    self.current_update.applied = True
                    #Add tag
            if self.current_update.applied:
                if self.current_update.over():
                    listener = get_app_listener()
                    listener.add_completed_update(self.current_update.name)
                    self.current_update = None
                    self.finish()
                    



        
        

