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

"""pymoult.lowlevel.data_update.py
   Published under the GPLv2 license (see LICENSE.txt)

   This module provides low level tools for updating data (updating
   data structures and converting objects)

"""

import sys

def updateToClass(obj,nclass,transformer=None):
    obj.__class__ = nclass
    if transformer != None:
        transformer(obj)

def generateMixinUser(class1,*mixins):
    class MixinUser(class1):
        pass
    MixinUser.__bases__ = mixins+(class1,)
    return MixinUser

def applyMixinToObject(obj,*mixins):
    class NewClass(type(obj)):
        pass
    NewClass.__bases__ = mixins+(type(obj),)
    obj.__class__ = NewClass

def addFieldToClass(cls,name,field):
    clas.name = field

def redefineClass(tclass,nclass):
    tname = tclass.__name__
    tmod = tclass.__module__
    if not tname in dir(sys.modules[tmod]):
        raise ValueError("class "+tname+" is not a toplevel class")
    setattr(sys.modules[tmod],tname,nclass)
    setattr(nclass,"__name__",tname)
    



