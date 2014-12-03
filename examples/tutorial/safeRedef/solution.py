#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
import sys
import time


main = sys.modules["__main__"]


def foo():
    print("foo")

def bar():
    print("bar")


update = SafeRedefineUpdate(main.manager,{main.say_hello:[main,foo]})

update.setup()
update.apply()
update.wait_update()

print("update step 1 complete")

time.sleep(3)

update = SafeRedefineUpdate(main.manager,{main.say_hello:[main,bar]})

update.setup()
update.apply()
update.wait_update()

print("update step 2 complete")
