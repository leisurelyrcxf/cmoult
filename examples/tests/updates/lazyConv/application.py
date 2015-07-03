#/usr/bin/python-dsu3

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener,log
import threading
import time
import random

class Item(object):
    def __init__(self,name,color):
        self.name = name
        self.color = color

    def display(self):
        log(0,"An item named "+self.name+" of color "+self.color)

    def change(self,color):
        self.color = color


def main():
    items = [Item("apple","red"),Item("banana","yellow"),Item("mango","green")]
    for x in range(5):
        for i in items:
            i.display()
        time.sleep(1)
            


thread = threading.Thread(target=main,name="app")
manager = ThreadedManager(name='global',threads=[thread])
manager.start()
thread.start()
listener = Listener()
listener.start()

thread.join()
manager.stop()
listener.stop()



