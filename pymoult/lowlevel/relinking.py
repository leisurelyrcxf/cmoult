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

"""pymoult.lowlevel.relinking.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides low level tools for relinking new functions
"""

from tputil import make_proxy
import sys

#Proxys
class ProxyManager(object):
    def __init__(self,obj):
        self.obj = obj

    def reroute(self,obj):
        self.obj = obj        
        self.proxy = make_proxy(self.controller,type(self.obj),self.obj)
        return self.proxy

    
    def controller(self,operation):
        if operation.opname == "__getattribute__" and operation.args[0] == "proxy_controller":
            return self
        if operation.opname == "__getattribute__" and (operation.args[0] not in type(operation.obj).__dict__) and (operation.args[0] not in [A.__dict__ for A in type(operation.obj).__bases__]):
            return operation.obj.__getattribute__(operation.args[0])
        operation.delegate()

    def generate(self):
        self.proxy = make_proxy(self.controller,type(self.obj),self.obj)
        return self.proxy


def proxify(obj):
    return ProxyManager(obj).generate()

def rerouteProxy(proxy,obj):
    return proxy.proxy_controller.reroute(obj)

def redefineFunction(tfunction,nfunction):
        tname = tfunction.__name__
        tmod = tfunction.__module__
        if not tname in dir(sys.modules[tmod]):
            raise ValueError("function "+tname+" is not toplevel")
        setattr(sys.modules[tmod],tname,nfunction)


def redirectPointer(pointer,target):
        pass
