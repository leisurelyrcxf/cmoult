#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import forceQuiescence
from pymoult.lowlevel.relinking import redefineFunction
import sys


main = sys.modules["__main__"]


def say_hi():
    print("hi")


class ForcedRedefinition(Update):
    def requirements(self):
        return True
    def alterability(self):
        self.continu = forceQuiescence(main,main.say_hello)
        print("say hello is now quiescent")
        return True
    def apply(self):
        redefineFunction(main,main.say_hello,say_hi)
    def over(self):
        self.continu.set()
        return True

    
update = ForcedRedefinition()
main.manager.add_update(update)


