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


class BasicUpdate(Update):
    """Basic update class that works well with the Basic Manager"""
    def __init__(self,manager,alterability,update):
        self.alterability = alterability
        self.update = update
        super(BasicUpdate,self).__init__(manager=manager)

    def setup(self):
        self.manager.is_alterable = self.alterability
        self.manager.update_function = self.update
        
    def apply(self):
        self.manager.update_triggered = True



