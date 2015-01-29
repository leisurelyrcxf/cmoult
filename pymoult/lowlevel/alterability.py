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

from pymoult.lowlevel.stack import resumeThread
from pymoult.lowlevel.relinking import redefineFunction
import threading
import time
import sys

def get_current_frames():
    """Returns a dictionary mapping the current frame of each thread to its id""" 
    return sys._current_true_frames()

def isFunctionInStack(func,thread):
    """Takes a function and a thread object as arguments. Returns True if
the function is in the stack of the given thread, False either."""    
    stack = get_current_frames()[thread.ident]
    x = stack
    while x is not None:
        if x.f_code is func.func_code:
            return True
        x = x.f_back
    return False

def isFunctionInAnyStack(func,threads=None):
    """Takes a function as argument. Returns True if the function is in the stack of any of the given threads, False either. If threads is None, checks the presence of func in all existing threads"""
    if threads is not None:
        stacks = [get_current_frames()[t.ident] for t in threads]
    else:
        stacks = get_current_frames().values()
    for stack in stacks:
        x = stack
        while x is not None:
            if x.f_code is func.func_code:
                return True
            x = x.f_back
    return False

def staticUpdatePoint(name=None):
    """Indicates a static update point in the code"""
    thread = threading.current_thread()
    #if name is not None and thread.last_update_point == name:
    thread.start_update()

def waitStaticPoints(threads):
    """Takes a list of threads as arguments. wait for each of them to reach a static point"""
    for thread in threads:
        thread.pause_event = threading.Event()
        thread.pause_event.clear()
        thread.static_point_event = threading.Event()
        thread.static_point_event.clear()
    for thread in threads:
        thread.static_point_event.wait()
        delattr(thread,"static_point_event")

def forceQuiescence(module,function):
    quiescent = threading.Event()
    quiescent.clear()
    can_continue = threading.Event()
    can_continue.clear()
    def stub(*args,**kwargs):
        can_continue.wait()
        return function(*args,**kwargs)
    def watch():
        while isFunctionInAnyStack(function):
            time.sleep(1)
        quiescent.set()
    watcher = threading.Thread(name=function.__name__+" watcher",target=watch)
    redefineFunction(module,function,stub)
    watcher.start()
    quiescent.wait()
    return can_continue
    
