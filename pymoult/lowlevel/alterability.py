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
import threading
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

def isFunctionInAnyStack(func):
    """Takes a function as argument. Returns True if the function is in teh stack of any thread, False either."""
    stacks = get_current_frames()
    for stack in stacks.values():
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

def wait_static_points(threads):
    """Takes a list of threads as arguments. wait for each of them to reach a static point"""
    for thread in threads:
        thread.pause_event = threading.Event()
        thread.pause_event.clear()
        thread.static_point_event = threading.Event()
        thread.static_point_event.clear()
    for thread in threads:
        thread.static_point_event.wait()
        delattr(thread,"static_point_event")



