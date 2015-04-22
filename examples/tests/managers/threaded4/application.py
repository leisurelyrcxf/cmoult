#/usr/bin/pypy-dsu

#Testing failed alterability

from pymoult.highlevel.managers import ThreadedManager
from pymoult.threads import DSU_Thread
from pymoult.highlevel.listener import Listener,log
import time
import threading
import sys
  
def func_v1():
    log(0,"v1")

def main():
    for x in range(8):
        time.sleep(1)
        func_v1()


thread = DSU_Thread(target=main,name="app")
thread.start()
#We want main to be run only once
thread.stop()
manager = ThreadedManager(name="pymoult",threads=[thread])
manager.start()

listener = Listener()
listener.start()

thread.join()
manager.stop()
listener.stop()

