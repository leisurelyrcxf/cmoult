#/usr/bin/python-dsu3

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener
import time
  
def tic():
    print("tic")

def tac():
    print("tac")

def main():
    while True:
        time.sleep(1)
        tic()
        time.sleep(1)
        tac()

manager = ThreadedManager(name='Manager')
manager.start()
listener = Listener()
listener.start()
main()
