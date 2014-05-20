#    updates.py This file is part of Pymoult
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

"""pymoult.updates.py
   Published under the GPLv2 license (see LICENSE.txt)

"""


class UpdateDefinitionError(Exception):
    def __init__(self,message):
        super(UpdateDefinitionError,self).__init__()
        self.message = message


class Update(object):
    def __init__(self,manager=None):
        self.manager = manager
    
    def setup(self):
        raise UpdateDefinitionError("You should define your own Update-based class")

    def apply(self):
       raise UpdateDefinitionError("You should define your own Update-based class")


class ThreadedUpdate(Update):
    """Update class that works with the Threaded Manager"""
    def __init__(self,manager):
        super(ThreadedUpdate,self).__init__(manager=manager)

    def setup(self):
        pass
      
    def apply(self):
        self.manager.invoke()

    def wait_update(self):
        self.manager.wait_over() 


class SafeRedefineUpdate(ThreadedUpdate):
    def __init__(self,manager,functions):
        self.functions = functions
        super(SafeRedefineUpdate,self).__init__(manager=manager)

    def setup(self):
        for function in self.functions.keys():
            self.manager.add_function(function,self.functions[function])
    
class EagerConversionUpdate(Update):
    def __init__(self,manager,cls,transformer):
        self.cls=cls
        self.transformer = transformer
        super(EagerConversionUpdate,self).__init__(manager=manager)
    
    def setup(self):
        self.manager.cls = self.cls
        self.manager.transformer = self.transformer

    def apply(self):
        self.manager.run()

    def wait_update(self):
        pass


class LazyConversionUpdate(ThreadedUpdate):
    def __init__(self,manager,cls,transformer,ending):
        self.cls=cls
        self.transformer = transformer
        self.ending = ending
        super(LazyConversionUpdate,self).__init__(manager=manager)

    def setup(self):
        self.manager.cls = self.cls
        self.manager.transformer = self.transformer
        self.manager.ending.ending = self.ending



