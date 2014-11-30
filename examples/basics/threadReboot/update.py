#parsed

from pymoult.highlevel.updates import ThreadRebootUpdate
from pymoult.lowlevel.alterability import wait_static_points
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


update = ThreadRebootUpdate(main.manager,[(main.thread,new_main,[])])

wait_static_points([main.thread])
update.setup()
update.apply()
update.wait_update()
resumeThread(main.thread)
print("update complete")
    


    

