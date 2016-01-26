#/usr/bin/python-dsu3

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener
import time

class Data(object):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return str(self.value)

def main():
    data = [Data(x) for x in range(5)]
    while True:
        time.sleep(2)
        for d in data:
            print(d)

manager = ThreadedManager(name='Manager')
manager.start()
listener = Listener()
listener.start()
main()
