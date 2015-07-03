#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate,Update
from pymoult.lowlevel.alterability import setupWaitStaticPoints,waitStaticPoints,cleanFailedStaticPoints,staticUpdatePoint
from pymoult.highlevel.listener import log
import sys

main = sys.modules["__main__"]

def func_v2():
    staticUpdatePoint()
    log(0,"v2")

class FailedAlterability(Update):
    def preupdate_setup(self):
        setupWaitStaticPoints([main.thread])
        print("1")
    def wait_alterability(self):
        print("2")
        return waitStaticPoints([main.thread])
    def clean_failed_alterability(self):
        print("3")
        cleanFailedStaticPoints([main.thread])
    def apply(self):
        pass

        
update1 = FailedAlterability(name="alterability")
update2 = SafeRedefineUpdate(main,main.func_v1,func_v2,name="func")
main.manager.add_update(update1)
main.manager.add_update(update2)

