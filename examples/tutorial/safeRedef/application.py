#/usr/bin/pypy-dsu


from pymoult.highlevel.managers import SafeRedefineManager
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

manager = SafeRedefineManager([thread])
manager.start()

listener = Listener()
listener.start()
