
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

"""pymoult.lowlevel.stack.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides low level tools for manipulating the stack 
"""

from  pymoult.threads import set_thread_trace, RebootException
import threading
import sys

########################
# Low level mechanisms #
########################

#Thread rebooting

#Update.apply
def resetThread(thread):
    """Reboots the given thread"""
    #enable rebooting for the thread
    thread.allow_reboot()
    def trace(frame,event,arg):
        raise RebootException()
    set_thread_trace(thread,trace)
    

#Update.apply
def switchMain(thread,func,args=[]):
    """Changes the "main" function of the given thread"""
    def m():
        return func(*args)
    thread.main = m

#Function rebooting

#Update.apply
def rebootFunction(thread,function,new_function,capture_state):
    """Reboots the current running function in given thread, capturing its
    state and calling a new function with it instead. Because the call
    to new_function, happens inside a trace, bear in mind that until
    that function returns, DSU mechanisms won't be usable for that thread."""
    def trace(frame,event,arg):
        #We check if the function we entered into was called by the
        #function to reboot
        if frame.f_back.f_code == function.func_code:
            state = capture_state(frame.f_back)
            res = new_function(state)
            sys.drop_frames(3,res)
        elif frame.f_code == function.func_code:
            state = capture_state(frame)
            res = new_function(state)
            sys.drop_frames(3,res)
        return trace
    set_thread_trace(thread,trace)




