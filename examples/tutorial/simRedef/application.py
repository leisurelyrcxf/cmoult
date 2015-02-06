#/usr/bin/pypy-dsu
from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener
import time
import threading
import random

shared = None
shared_lock = threading.Lock()

def read_shared():
    shared_lock.acquire()
    time.sleep(1)
    print("Value of shared : "+str(shared))
    shared_lock.release()


def write_shared():
    global shared
    shared_lock.acquire()
    time.sleep(1)
    shared = random.randint(0,10)
    shared_lock.release()

def reader_f():
    while True:
        time.sleep(0.3)
        read_shared()

def writer_f():
    while True:
        time.sleep(0.5)
        write_shared()
        

writer = threading.Thread(target=writer_f)
writer.start()
reader = threading.Thread(target=reader_f)
reader.start()

manager = ThreadedManager(reader,writer)
manager.set_sleepTime(0.5)
manager.start()

listener = Listener()
listener.start()
