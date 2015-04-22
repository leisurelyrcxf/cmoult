#parsed

from pymoult.highlevel.updates import ThreadRebootUpdate
from pymoult.lowlevel.alterability import waitStaticPoints,setupWaitStaticPoints,cleanFailedStaticPoints
from pymoult.highlevel.listener import log
from threading import current_thread
import sys
import time


main = sys.modules["__main__"]


def func_v2():
    log(0,"v2")

def new_main():
    #We want the thread to run only once.
    current_thread().stop()
    for x in range(2):
        time.sleep(1)
        func_v2()
        


class CustomUpdate(ThreadRebootUpdate):
    def preupdate_setup(self):
        setupWaitStaticPoints([main.thread])

    def wait_alterability(self):
        return waitStaticPoints([main.thread])

    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.thread])

update = CustomUpdate(main.thread,new_main,[],name="thread")
main.manager.add_update(update)


    


    

