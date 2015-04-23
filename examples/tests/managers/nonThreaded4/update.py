#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate,Update,isApplied
from pymoult.highlevel.listener import log
import sys

main = sys.modules["__main__"]

def func_v2():
    log(0,"v2")


class FailedAlterability(Update):
    def check_alterability(self):
        return main.func_v1 == func_v2

    def apply(self):
        pass
    
update1 = FailedAlterability(name="alterability")
update1.set_max_tries(3)
update2 = SafeRedefineUpdate(main,main.func_v1,func_v2,name="func")
main.manager.add_update(update1)
main.manager.add_update(update2)


