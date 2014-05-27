#parsed

from pymoult.highlevel.updates import ThreadRebootUpdate
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

update.setup()
update.apply()
update.wait_update()

print("update complete")
