#/usr/bin/python-dsu3

from pymoult.threads import DSU_Thread
from pymoult.highlevel.listener import Listener
import time

  
def hello():
    print("hello")

def main():
    while True:
        time.sleep(1)
        hello()


thread = DSU_Thread(target=main,name="main")
thread.start()
listener = Listener()
listener.start()
