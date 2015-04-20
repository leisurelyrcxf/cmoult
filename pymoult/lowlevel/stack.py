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

def suspendThread(thread):
    """Suspends the given thread"""
    if not hasattr(thread,"pause_event"):
        thread.pause_event = threading.Event()
        thread.pause_event.clear()
        def trace(frame,event,arg):
            if hasattr(thread,"pause_event"):
                thread.pause_event.wait()
            return None
        set_thread_trace(thread,trace)

def resumeThread(thread):
    """resumes the execution fo the given thread if it is suspended"""
    if hasattr(thread,"pause_event"):
        thread.pause_event.set()
        delattr(thread,"pause_event")
        set_thread_trace(thread,None)

########################
# Low level mechanisms #
########################

#Update.apply
def resetThread(thread):
    """Reboots the given thread"""
    def trace(frame,event,arg):
        raise RebootException()
    set_thread_trace(thread,trace)

#Update.apply
def switchMain(thread,func,args=[]):
    """Changes the "main" function of the given thread"""
    def m():
        return func(*args)
    thread.main = m

