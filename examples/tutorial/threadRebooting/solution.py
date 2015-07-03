#parsed

from pymoult.highlevel.updates import ThreadRebootUpdate
from pymoult.lowlevel.alterability import waitStaticPoints,setupWaitStaticPoints,cleanFailedStaticPoints
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
    def preupdate_setup(self):
        setupWaitStaticPoints([main.thread])


    def wait_alterability(self):
        return waitStaticPoints([main.thread])

    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.thread])

update = CustomUpdate(main.thread,new_main,[])
main.manager.add_update(update)


    


    

