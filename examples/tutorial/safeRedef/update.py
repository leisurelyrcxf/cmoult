#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
import sys


main = sys.modules["__main__"]

def say_hi():
    print("hi")


update = SafeRedefineUpdate(main,main.say_hello,say_hi)
main.manager.add_update(update)


