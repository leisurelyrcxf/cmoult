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

import threading


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
    

class BasicManager(Manager):
    """Manager at application level that can handles every update
    in its own thread if the update developper provides the whole update code"""

    def __init__(self):
        self.ownThread = None
        self.update_triggered = False
        self.stop = False
        super(BasicManager).__init__()

    def update_function(self):
        pass

    def thread_main(self):
        while not self.stop:
            if self.update_triggered:
                if self.is_alterable():
                    self.update_function()
                    self.update_triggered = False

    def start(self):
        self.ownThread = threading.Thread(target=self.thread_main)
        self.ownThread.start()


