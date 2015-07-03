#/usr/bin/python-dsu3

from pymoult.highlevel.managers import Manager
from pymoult.highlevel.listener import Listener,log
import time
import threading
import sys
  
def func_v1():
    log(0,"v1")

manager = Manager(name="pymoult")

def main():
    for x in range(5):
        manager.apply_next_update()
        time.sleep(1)
        func_v1()




listener = Listener()
listener.start()

main()

listener.stop()

