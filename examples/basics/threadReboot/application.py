#/usr/bin/pypy-dsu


from pymoult.highlevel.managers import ThreadRebootManager
from pymoult.threads import DSU_Thread
from pymoult.highlevel.listener import Listener
import time

  
def say_hello():
    print("hello")

def main():
    while True:
        time.sleep(2)
        say_hello()


thread = DSU_Thread(target=main,name="main")
thread.start()

manager = ThreadRebootManager()
manager.start()

listener = Listener()
listener.start()
