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
"""

import threading
from pymoult.lowlevel.stack import *
from pymoult.lowlevel.relinking import *
from pymoult.lowlevel.alterability import *
from pymoult.threads import *
import time
import Queue

class Manager(object):
    def __init__(self,sleepTime=3,**units):
        for element in units.keys():
            setattr(self,element,units[element])
        self.invoked = threading.Event()
        self.over = threading.Event()
        self.sleepTime=sleepTime

    def start(self):
        pass

    def pause_threads(self):
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in self.threads:
                suspendThread(t)

    def resume_threads(self):
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in self.threads:
                resumeThread(t)
        
    def is_alterable(self):
        return False

    def is_over(self):
        return False

    def invoke(self):
        self.invoked.set()

    def finish(self):
        self.over.set()
        self.invoked.clear()
    
    def begin(self):
        self.over.clear()

    def wait_over(self):
        self.over.wait()
    
class ThreadedManager(Manager):
    """Manager using its owwn thread to monitor alterabilty and apply the
       update"""

    def __init__(self,sleepTime=3,**units):
        self.ownThread = None
        self.stop = False
        super(ThreadedManager,self).__init__(sleepTime=sleepTime,**units)

    def update_function(self):
        pass

    def thread_main(self):
        while not self.stop:
            self.invoked.wait()
            self.begin()
            if self.is_alterable():
                self.update_function()
                while not self.is_over():
                    time.sleep(self.sleepTime)
                self.finish()

    def start(self):
        self.ownThread = threading.Thread(target=self.thread_main)
        self.ownThread.start()


class SafeRedefineManager(ThreadedManager):
    """Manager for handling safe redefinition update"""

    def __init__(self,threads,sleepTime=3):
        self.functions = Queue.Queue()
        super(SafeRedefineManager,self).__init__(sleepTime=sleepTime,threads=threads)

    def is_alterable(self,function):
        for thread in self.threads:
            if isFunctionInStack(function,thread):
                return False
        return True
  
    def add_function(self,function,new_function):
        self.functions.put((function,new_function))

    def thread_main(self):
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
                    if self.is_alterable(function[0]):
                        self.pause_threads()
                        redefineFunction(function[0],function[1])
                        function_updated = True
                        self.resume_threads()
                    time.sleep(self.sleepTime)
     

                        



            
