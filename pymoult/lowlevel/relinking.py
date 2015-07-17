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

########################
# Low level mechanisms #
########################

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
