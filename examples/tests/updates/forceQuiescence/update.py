#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import waitForceQuiescence,setupForceQuiescence,cleanForceQuiescence,cleanFailedForceQuiescence
from pymoult.lowlevel.relinking import redefineFunction
from pymoult.highlevel.listener import log
import sys


main = sys.modules["__main__"]


def func_v2():
    log(0,"v2")


class ForcedRedefinition(Update):
    def preupdate_setup(self):
        q,c,w = setupForceQuiescence(main,main.func_v1)
        self.quiescent_event = q
        self.continue_event = c
        self.watcher = w
        
    def wait_alterability(self):
        return waitForceQuiescence(self.quiescent_event)

    def apply(self):
        redefineFunction(main,main.func_v1,func_v2)
        
    def preresume_setup(self):
        cleanForceQuiescence(self.continue_event)

    def cleanFailedForceQuiescence(self):
        cleanFailedForceQuiescence(self.continue_event,self.watcher,main,main.func_v1)
    
update = ForcedRedefinition()
main.manager.add_update(update)


