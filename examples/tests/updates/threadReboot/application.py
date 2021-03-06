#/usr/bin/python-dsu3

from pymoult.highlevel.managers import ThreadedManager
from pymoult.threads import DSU_Thread
from pymoult.highlevel.listener import Listener,log
from pymoult.lowlevel.alterability import staticUpdatePoint
import time
import threading
import sys
  
def func_v1():
    log(0,"v1")

def main():
    for x in range(5):
        time.sleep(1)
        staticUpdatePoint()
        func_v1()


thread = DSU_Thread(target=main,name="app")
thread.start()
manager = ThreadedManager(name="pymoult",threads=[thread])
manager.start()
listener = Listener()
listener.start()

thread.join()
manager.stop()
listener.stop()

