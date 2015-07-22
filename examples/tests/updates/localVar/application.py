#/usr/bin/python-dsu3

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener,log
import time
import threading
import sys

def talk(n):
    text = "Hello!"
    if n>0:
        talk(n-1)
    time.sleep(1)
    log(0,text)

def main():
    talk(5)


thread = threading.Thread(target=main,name="app")
thread.start()
manager = ThreadedManager(name="pymoult",threads=[thread])
manager.start()

listener = Listener()
listener.start()

thread.join()
manager.stop()
listener.stop()

