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

"""pymoult.lowlevel.alterability.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module supplies low level tools for handling the alterability

"""

from pymoult.lowlevel.stack import resumeThread,suspendThread
from pymoult.lowlevel.relinking import redefineFunction
import threading
import inspect
import time
import sys

SLEEP_TIME = 5 #Time for sleeping before checking alterabilty again
WAIT_LIMIT = 10 #Number of alterability check done before failing

##############################
# Tools for inspecting stack #
##############################

def get_current_frames():
    """Returns a dictionary mapping the current frame of each thread to its id""" 
    return sys._current_true_frames()

def checkFinStack(func,stack):
    x = stack
    while x is not None:
        if x.f_code is func.func_code:
            return True
        x = x.f_back
    return False

############################
# Quiescence of a function #  
############################

#Update.check_alterability
def isFunctionInStack(func,thread):
    """Takes a function and a thread object as arguments. Returns True if
the function is in the stack of the given thread, False either."""    
    stack = get_current_frames()[thread.ident]
    return checkFinStack(func,stack)

#Update.check_alterability
def isFunctionInAnyStack(func,threads=None):
    """Takes a function as argument. Returns True if the function is in the stack of any of the given threads, False either. If threads is None, checks the presence of func in all existing threads"""
    if threads is not None:
        stacks = [get_current_frames()[t.ident] for t in threads]
    else:
        stacks = get_current_frames().values()
    result = False
    for stack in stacks:
        result = result or checkFinStack(func,stack)
    return result

#Update.wait_alterability
def waitQuiescenceOfFunction(func,threads=None):
    """Takes a function as argument. Returns when the function is not in
       the stack of any threads (or any of the given threads if the
       threads argument is not None). This function suspends
       threads. Returns True when alterability is reached, returns False if not."""
    alerable = False
    for x in range(WAIT_LIMIT):
        if threads is None:
            threads = threading.enumerate()
            #remove the current thread from the list of threads to be suspended
            threads.remove(threading.currentThread())
            stacks = get_current_frames().values()
        else:
            stacks = [get_current_frames()[t.ident] for t in threads]
        #We suspend all threads
        for t in threads:
            suspendThread(t)
        #We check if the function is in the stacks
        for stack in stacks:
            alterable = alterable or checkFinStack(func,stack)
            alterable = not alterable
        #If we are alterable, we return
        if alterable:
            return True
        else:
            #We resume the threads
            for t in threads:
                resumeThread(t)
        time.sleep(SLEEP_TIME)
    return False


#Force Quiescence, the three functions are needed (preupdate,alterability,preresume)

#Update.preupdate_setup
def setupForceQuiescence(module,function):
    quiescent = threading.Event()
    quiescent.clear()
    can_continue = threading.Event()
    can_continue.clear()
    def stub(*args,**kwargs):
        #We do not want to suspend if we are in a recursive call
        callers = [x[3] for x in inspect.stack()[1:]] 
        if function.__name__ in callers:
            return function(*args,**kwargs)
        can_continue.wait()
        return getattr(module,function.__name__)(*args,**kwargs)
    def watch():
        while isFunctionInAnyStack(function):
            time.sleep(SLEEP_TIME)
        quiescent.set()
    watcher = threading.Thread(name=function.__name__+" watcher",target=watch)
    redefineFunction(module,function,stub)
    watcher.start()
    return quiescent,can_continue

#Update.wait_alterability
def waitForceQuiescence(quiescent):
    quiescent.wait()

#Update.check_alterability
def checkForceQuiescence(quiescent):
    return quiescent._Event_flag

#Update.preresume_setup
def cleanForceQuiescence(can_continue):
    can_continue.set()


########################
# Static Update Points #
########################

#To be placed in the application code
def staticUpdatePoint(name=None):
    """Indicates a static update point in the code"""
    thread = threading.current_thread()
    thread.start_update()

#Update.preupdate_setup
def setupWaitStaticPoint(threads):
    for thread in threads:
        thread.pause_event = threading.Event()
        thread.pause_event.clear()
        thread.static_point_event = threading.Event()
        thread.static_point_event.clear()
    
#Update.wait_alterability    
def waitStaticPoints(threads):
    """Takes a list of threads as arguments. wait for each of them to reach a static point"""
    for thread in threads:
        thread.static_point_event.wait()
        delattr(thread,"static_point_event")

#Update.check_alterability
def CheckStaticPointReached(threads):
    for thread in threads:
        if not thread.static_point_event._Event_flag:
            return False
    for thread in threads:
        delattr(thread,"static_point_event")
    return True
            
