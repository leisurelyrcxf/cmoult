#/usr/bin/python-dsu

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener,log
from pymoult.lowlevel.alterability import staticUpdatePoint
from pymoult.threads import DSU_Thread
import time
import threading
import sys
  
def main():
    r = []
    for i in range(20):
        staticUpdatePoint()
        r.append(i)
        log(0,"v1 : "+str(i))
        time.sleep(0.5)

    

thread = DSU_Thread(target=main,name="app")
thread.start()
manager = ThreadedManager(name="pymoult",threads=[thread])
manager.start()

listener = Listener()
listener.start()

thread.join()
manager.stop()
listener.stop()

