#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.relinking import redefineFunction
from pymoult.lowlevel.alterability import waitStaticPoints,setupWaitStaticPoints,cleanFailedStaticPoints,resumeSuspendedThreads
import sys

main = sys.modules["__main__"]


def tic_v2():
    print("tic2")

def tac_v2():
    print("tac2")


class CustomUpdate(Update):
    def preupdate_setup(self):
        setupWaitStaticPoints([main.thread])

    def wait_alterability(self):
        return waitStaticPoints([main.thread])

    def apply(self):
        redefineFunction(main,main.tic,tic_v2)
        redefineFunction(main,main.tac,tac_v2)

    def resume_hook(self):
        resumeSuspendedThreads()
        
    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.thread])

    
update = CustomUpdate()
main.manager.add_update(update)

