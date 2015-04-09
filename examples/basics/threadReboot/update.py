#parsed

from pymoult.highlevel.updates import ThreadRebootUpdate
from pymoult.lowlevel.alterability import waitStaticPoints
from pymoult.lowlevel.stack import resumeThread
import sys
import time


main = sys.modules["__main__"]


def say_hi():
    print("hi")

def new_main():
    while True:
        time.sleep(2)
        say_hi()


class CustomUpdate(ThreadRebootUpdate):

    def alterability(self):
        waitStaticPoints([main.thread])
        return True

    def over(self):
        resumeThread(self.thread)
        return True


        
update = CustomUpdate(main.thread,new_main,[])
main.manager.add_update(update)


    


    

