#/usr/bin/pypy-dsu


from pymoult.manager import Manager
from pymoult.updates import Update
from pymoult.threads import DSU_Thread
from pymoult.listener import Listener
from pymoult.stack.tools import isFunctionInStack
import time
import threading


  
def say_hello():
    print("hello")



def main():
    while True:
        time.sleep(2)
        say_hello()



thread = DSU_Thread(target=main)
thread.start()


class UpManager(Manager):
    def __init__(self):
        self.threads = [thread]
        self.ownThread = threading.Thread(target=self.main)
        self.updateTriggered = False
        self.new_function = None

    def main(self):
        global say_hello
        while True:
            if self.updateTriggered:
                if not isFunctionInStack(say_hello,thread):
                    self.pause_threads()
                    say_hello = self.new_function
                    self.resume_threads()
                    self.updateTriggered = False


    def start(self):
        self.ownThread.start()



manager = UpManager()
manager.start()

listener = Listener()
listener.start()


class UpUpdate(Update):
    def __init__(self,new_function):
        self.new_function = new_function
        self.manager = manager

    def setup(self):
        self.manager.new_function = self.new_function
    
    def apply(self):
        self.manager.updateTriggered = True
