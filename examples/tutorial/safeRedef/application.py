#/usr/bin/python-dsu3


from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener
import time
import threading

  
def say_hello():
    print("hello")

def main():
    while True:
        time.sleep(2)
        say_hello()



thread = threading.Thread(target=main)
thread.start()

manager = ThreadedManager(name='Manager',threads=[thread])
manager.start()

listener = Listener()
listener.start()
