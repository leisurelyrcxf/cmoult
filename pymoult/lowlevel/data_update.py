#    data_update.py This file is part of Pymoult
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
import types

def generateMixinUser(class1,*mixins):
    """Creates a class based on the given class and the given mixins"""
    class MixinUser(class1):
        pass
    MixinUser.__bases__ = mixins+(class1,)
    return MixinUser

########################
# Low level mechanisms #
########################

#Update.apply
def applyMixinToObject(obj,*mixins):
    """Applies the given mixins to the given object"""
    class NewClass(type(obj)):
        pass
    NewClass.__bases__ = mixins+(type(obj),)
    obj.__class__ = NewClass

#Update.apply
def updateToClass(obj,cls,nclass,transformer=None):
    """Updates a given object to a given class. If a trasformer is given
    in argument, applies it to the object"""
    if cls == None or obj.__class__ == cls:
        obj.__class__ = nclass
    if transformer != None:
        transformer(obj)

#Update.apply
def addFieldToClass(cls,name,field):
    """Adds the given field to the given class under the given name"""
    setattr(cls,name,field)

#Update.apply
def addMethodToClass(cls,name,method):
    """Adds a method to the given class and binds it to the class"""
    setattr(cls,name,method)

#Update.apply
def redefineClass(module,tclass,nclass):
    """redfefines a given class from a given module so it is equals to a new class""" 
    tname = tclass.__name__
    setattr(module,tname,nclass)
    setattr(nclass,"__name__",tname)
