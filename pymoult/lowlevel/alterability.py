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

from pymoult.threads import start_active_update
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

def staticUpdatePoint():
    """Indicates a static update point in the code"""
    start_active_update()

