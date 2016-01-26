#parsed

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.updates import Update
from pymoult.lowlevel.stack import switchMain,resetThread
from pymoult.lowlevel.alterability import waitStaticPoints,setupWaitStaticPoints,cleanFailedStaticPoints
import sys
import time

main = sys.modules["__main__"]

def hello_v2():
    print("hello James")

def new_main():
    while True:
        time.sleep(1)
        hello_v2()


class CustomUpdate(Update):
    def preupdate_setup(self):
        setupWaitStaticPoints([main.thread])

    def wait_alterability(self):
        return waitStaticPoints([main.thread])

    def apply(self):
        switchMain(main.thread,new_main)
        resetThread(main.thread)
        main.thread.resume()

    
    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.thread])


manager = ThreadedManager()
manager.start()        
update = CustomUpdate()
manager.add_update(update)


    


    

