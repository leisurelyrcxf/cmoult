#    listener.py This file is part of Pymoult
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
"""pymoult.manager.py
   Published under the GPLv2 license (see LICENSE.txt)
"""
from pymoult.common.high_level import *

class Manager(object):
    def __init__(self,**units):
        for element in units.keys():
            setattr(self,element,units[element])

    def start(self):
        pass

    def pause_threads(self):
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in threads:
                pause_thread(t)

    def resume_threads(self):
        if hasattr(self,"threads") and type(self.threads) == list:
            for t in threads:
                resume_thread(t)
        

    def is_alterable(self):
        return False
    
