#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import setupWaitStaticPoints,waitStaticPoints,cleanFailedStaticPoints
from pymoult.lowlevel.stack import rebootFunction
from pymoult.highlevel.listener import log
import sys

main = sys.modules["__main__"]

def new_main(state):
    r = state[0]
    n = state[1]
    for i in range(20-n):
        print("lama")
        r.append(i+n)
        log(0,"v2 : "+str(i+n))
    log(0,str(r))

def capture_state(frame):
    n = frame.f_locals['i']
    r = frame.f_locals['r']
    return r,n

class BranchUpdate(Update):
    def preupdate_setup(self):
        setupWaitStaticPoints([main.thread])
    def wait_alterability(self):
        return waitStaticPoints([main.thread])
    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.thread])
    def apply(self):
        rebootFunction(main.thread,main.main,new_main,capture_state)


update = BranchUpdate(name="main")
main.manager.add_update(update)


