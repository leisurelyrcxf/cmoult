#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate,Update
from pymoult.lowlevel.alterability import setupWaitStaticPoints,waitStaticPoints,cleanFailedStaticPoints,staticUpdatePoint
from pymoult.highlevel.listener import log
import sys
import time

main = sys.modules["__main__"]

def func_v2():
    staticUpdatePoint()
    log(0,"v2")

class FailedAlterability(Update):
    def preupdate_setup(self):
        setupWaitStaticPoints([main.thread])
    def wait_alterability(self):
        return waitStaticPoints([main.thread])
    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.thread])
    def apply(self):
        pass

        
update1 = FailedAlterability(name="alterability")
update2 = SafeRedefineUpdate(main,main.func_v1,func_v2,name="func",threads=[main.thread])
update1.set_max_tries(10)
update1.set_sleep_time(0.1)
main.manager.add_update(update1)
main.manager.add_update(update2)

