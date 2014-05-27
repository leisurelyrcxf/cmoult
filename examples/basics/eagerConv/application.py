#/usr/bin/pypy-dsu

from pymoult.highlevel.managers import EagerConversionManager
from pymoult.highlevel.listener import Listener
import threading
import time
import random



class Item(object):
    def __init__(self,name,color):
        self.name = name
        self.color = color

    def display(self):
        print("An item named "+self.name+" of color "+self.color)

    def change(self,color):
        self.color = color





def main():
    items = [Item("apple","red"),Item("banana","yellow"),Item("mango","green")]
    colors = ["orange","pink","blue","purple","yellow","white"]
    while True:
        for i in items:
            i.display()
            i.change(random.choice(colors))
        time.sleep(2)
            


thread = threading.Thread(target=main)
manager = EagerConversionManager(threads=[thread])
manager.start()
thread.start()
listener = Listener()
listener.start()


