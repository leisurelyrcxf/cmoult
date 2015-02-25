#/usr/bin/pypy-dsu


from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener
import time
import threading

  
def say_tic():
    print("tic")

def say_tac():
    print("tac")

def main():
    while True:
        time.sleep(2)
        say_tic()
        time.sleep(1)
        say_tac()



thread = threading.Thread(target=main)
thread.start()

manager = ThreadedManager(thread)
manager.start()

listener = Listener()
listener.start()
