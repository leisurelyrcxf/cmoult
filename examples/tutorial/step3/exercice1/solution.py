#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import waitQuiescenceOfFunction,resumeSuspendedThreads
from pymoult.lowlevel.relinking import redefineFunction
from pymoult.highlevel.managers import ThreadedManager
import sys

main = sys.modules["__main__"]

def hello_v2():
    print("Hello James")


class CustomUpdate(Update):
    def wait_alterability(self):
        return waitQuiescenceOfFunction(main.hello)
    def resume_hook(self):
        resumeSuspendedThreads()
    def apply(self):
        redefineFunction(main,main.hello,hello_v2)

    
manager = ThreadedManager()
manager.start()
update = CustomUpdate()

manager.add_update(update)

