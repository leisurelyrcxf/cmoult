#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
import sys


main = sys.modules["__main__"]


def say_hi():
    print("hi")


update = SafeRedefineUpdate(main.manager,{main.say_hello:[main,say_hi]})

update.setup()
update.apply()
update.wait_update()

print("update complete")
