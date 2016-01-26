#/usr/bin/python-dsu3

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.listener import Listener
from pymoult.lowlevel.alterability import staticUpdatePoint
from pymoult.threads import DSU_Thread
import time
  
def tic():
    print("tic")

def tac():
    print("tac")

def main():
    while True:
        staticUpdatePoint()
        time.sleep(1)
        tic()
        time.sleep(1)
        tac()
        

        
manager = ThreadedManager(name='Manager')
manager.start()
listener = Listener()
listener.start()
thread = DSU_Thread(target=main)
thread.start()
