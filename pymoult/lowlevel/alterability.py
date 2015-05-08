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
import inspect


#Getting values form an update object by inspecting the stack
def getUpdateWaitValues():
    """If the caller is being called from a "wait_alterability" method of
    an update, returns the values of that update's "max_tries" and
    "sleep_time" attributes. Else, we return default values"""
    caller = inspect.getouterframes(inspect.currentframe())[2]
    if caller[3] == "wait_alterability" or caller[3] == "preupdate_setup":
        update = inspect.getargvalues(caller[0])[3]['self']
        return (update.max_tries,update.sleep_time)
    return (10,2)


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

#Update.check_alterability
def checkQuiescenceOfFunction(func,threads=[]):
    """Takes a function as argument. Returns True if the function is in the stack of any threads (or any of the given threads if the threads argument is not None). This function suspends
       threads."""
    if threads == []:
        threads = threading.enumerate()
        #remove the current thread from the list of threads to be suspended
        threads.remove(threading.currentThread())
    #We suspend all threads
    for t in threads:
        suspendThread(t)
    #Then we capture the stacks
    stacks = [get_current_frames()[t.ident] for t in threads]
    #We check if the function is in the stacks
    finstack = False
    for stack in stacks:
        finstack = finstack or checkFinStack(func,stack)
        #If function is not in the stack, we return
    if not finstack:
        return True
    else:
        #We resume the threads
        for t in threads:
            resumeThread(t)

#Update.wait_alterability
def waitQuiescenceOfFunction(func,threads=[]):
    """Takes a function as argument. Returns when the function is not in
       the stack of any threads (or any of the given threads if the
       threads argument is not None). This function suspends
       threads. Returns True when alterability is reached, returns False if not."""
    #If we are called in a wait_alterability method, we get the
    #max_tries and sleep_times attributes of the update object.
    max_tries, sleep_time = getUpdateWaitValues()
    finstack = False
    if threads == []:
        threads = threading.enumerate()
        #remove the current thread from the list of threads to be suspended
        threads.remove(threading.currentThread())
    for x in range(max_tries):
        #We suspend all threads
        for t in threads:
            suspendThread(t)
        #Then we capture the stacks
        stacks = [get_current_frames()[t.ident] for t in threads]
        #We check if the function is in the stacks
        for stack in stacks:
            finstack = finstack or checkFinStack(func,stack)
        #If function is not in the stack, we return
        if not finstack:
            return True
        else:
            #We resume the threads
            for t in threads:
                resumeThread(t)
        time.sleep(sleep_time)
    return False

#Update.resume_hook
def resumeSuspendedThreads(threads=[]):
    """If a empty list of threads was given to waitQuiescenceOfFunction,
    it will suspend allmost all threads, which may not be handle by
    the manager. We need to resume these threads during the resume_hook."""
    if threads == []:
        threads = threading.enumerate()
        #remove the current thread from the list of threads to be resumed
        threads.remove(threading.currentThread())
    for thread in threads:
        resumeThread(thread)

#Force Quiescence

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
    class QuiescenceWatcher(threading.Thread):
        def __init__(self):
            self.watching = True
            super(QuiescenceWatcher,self).__init__()
            self.name=function.__name__+" watcher"

        def run(self):
            while self.watching and isFunctionInAnyStack(function):
                time.sleep(sleep_time)
            quiescent.set()
    watcher = QuiescenceWatcher()
    redefineFunction(module,function,stub)
    watcher.start()
    return quiescent,can_continue,watcher

#Update.wait_alterability
def waitForceQuiescence(quiescent):
    max_tries,sleep_time = getUpdateWaitValues()
    timeout = max_tries*sleep_time
    return quiescent.wait(timeout)

#Update.check_alterability
def checkForceQuiescence(quiescent):
    return quiescent._Event__flag

#Update.preresume_setup
def cleanForceQuiescence(can_continue):
    can_continue.set()

#Update.clean_failed_alterability
def cleanFailedForceQuiescence(can_continue,watcher,module,function):
    """cleans up if failed to force quiescence. Function is the original
    function"""
    #First we stop the watcher
    watcher.watching = False
    #Then we switch back the the function to remove the stub
    redefineFunction(module,function,function)
    #Now, we can makeevryone leave the stub
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
def setupWaitStaticPoints(threads):
    for thread in threads:
        thread.pause_event = threading.Event()
        thread.pause_event.clear()
        thread.static_point_event = threading.Event()
        thread.static_point_event.clear()
    
#Update.wait_alterability    
def waitStaticPoints(threads):
    """Takes a list of threads as arguments. wait for each of them to reach a static point"""
    #boolean that will be true if the static point has been reached,
    #false if we timed-out
    max_try,sleep_time = getUpdateWaitValues()
    timeout = max_try*sleep_time
    for thread in threads:
        if thread.static_point_event.wait(timeout):
            delattr(thread,"static_point_event")
        else:
            return False
    return True

#Update.check_alterability
def checkStaticPointsReached(threads):
    for thread in threads:
        if not thread.static_point_event._Event__flag:
            return False
    for thread in threads:
        delattr(thread,"static_point_event")
    return True

#Update.clean_failed_alterability
def cleanFailedStaticPoints(threads):
    #Threads may have been suspended, so we need them to resume.  If
    #the thread had a pause_event be never reached the point,
    #resumeThread will still clean it up
    for t in threads:
        #First, we delete the static_point_event too
        delattr(t,"static_point_event")
        resumeThread(t)

#Update.resume_hook
#resumeSuspendedThreads

#If the threads supplied in setupWaitStaticPoints were not included in
#the threads handled by the manager or the update, they need to be
#resumed at that point. So the resumeSuspendedThreads function should
#be used in Update.resume_hook
