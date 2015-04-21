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
    """Proxy class that will handle a proxy to a given object"""

    def __init__(self,obj):
        """Constructor"""
        self.obj = obj

    def reroute(self,obj):
        """Reroutes the proxy to another fiven object"""
        self.obj = obj        
        self.proxy = make_proxy(self.controller,type(self.obj),self.obj)
        return self.proxy

    
    def controller(self,operation):
        """Controller for the proxy. Allows access to the ProxyManager
        throught the "proxy_controller" attribute."""
        if operation.opname == "__getattribute__" and operation.args[0] == "proxy_controller":
            return self
        if operation.opname == "__getattribute__" and (operation.args[0] not in type(operation.obj).__dict__) and (operation.args[0] not in [A.__dict__ for A in type(operation.obj).__bases__]):
            return operation.obj.__getattribute__(operation.args[0])
        operation.delegate()

    def generate(self):
        """Generates the proxy to the object and returns it""" 
        self.proxy = make_proxy(self.controller,type(self.obj),self.obj)
        return self.proxy


def proxify(obj):
    """Returns a proxy to the given object"""
    return ProxyManager(obj).generate()


########################
# Low level mechanisms #
########################

#Update.apply
def rerouteProxy(proxy,obj):
    """Reroutes the given proxy so that it targets the given object"""
    return proxy.proxy_controller.reroute(obj)

#Update.apply
def redefineFunction(module,tfunction,nfunction):
    """Redefines a given function from a given module so that it is eaqual
    to the given new one"""
    tfname = tfunction.__name__
    setattr(module,tfname,nfunction)
    setattr(nfunction,"__name__",tfname)

def redirectPointer(pointer,target):
    """Not implemented yet"""
    pass
