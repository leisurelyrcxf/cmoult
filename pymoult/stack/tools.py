#    tools.py This file is part of Pymoult
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
"""pymoult.stack.tools.py
   Published under the GPLv2 license (see LICENSE.txt)
"""

from  pymoult.threads import set_thread_trace, get_current_frames


def resetThread(thread):
    def trace(frame,event,arg):
        raise RebootException()
    set_thread_trace(thread,trace)

def switchMain(thread,func,args=[]):
    def m():
        return func(*args)
    thread.main = m

def isFunctionInStack(func,thread):
    stack = get_current_frames()[thread.ident]
    x = stack
    while x is not None:
        if x.f_code is func.func_code:
            return True
        x = x.f_back
    return False


def isFunctionInAllStack(func):
    stacks = get_current_frames()
    for stack in stacks.values():
        x = stack
        while x is not None:
            if x.f_code is func.func_code:
                return True
            x = x.f_back
    return False
