#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
import sys
import time


main = sys.modules["__main__"]


def foo():
    print("foo")

def bar():
    print("bar")


class CustomUpdate(SafeRedefineUpdate):
    def alterability(self):
        time.sleep(3)
        return super(CustomUpdate,self).alterability()

    
update1 = SafeRedefineUpdate(main,main.say_hello,foo)
update2 = CustomUpdate(main,main.say_hello,bar)

main.manager.add_update(update1)
main.manager.add_update(update2)

