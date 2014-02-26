#/usr/bin/pypy-dsu


from pymoult.manager import SafeRedefineManager
from pymoult.threads import DSU_Thread
from pymoult.listener import Listener
import time


  
def say_hello():
    print("hello")



def main():
    while True:
        time.sleep(2)
        say_hello()



thread = DSU_Thread(target=main)
thread.start()

manager = SafeRedefineManager([thread])
manager.start()

listener = Listener()
listener.start()
