#/usr/bin/python-dsu3

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import PipeListener,log
import time
import threading
import sys
  
def func_v1():
    log(0,"v1")

def main():
    for x in range(5):
        time.sleep(1)
        func_v1()

thread = threading.Thread(target=main,name="app")
thread.start()
manager = ThreadedManager(name="pymoult",threads=[thread])
manager.start()

listener = PipeListener(path="fifopipe")
listener.start()

thread.join()
listener.stop()
manager.stop()
