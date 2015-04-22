#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate,Update
from pymoult.highlevel.listener import log
import sys

main = sys.modules["__main__"]

def func_v2():
    log(0,"v2")


class FailedRequirements(Update):
    def check_requirements(self):
        return "never"
    def wait_alterability(self):
        return True
    def apply(self):
        pass

update1 = FailedRequirements(name="requirements")
update2 = SafeRedefineUpdate(main,main.func_v1,func_v2,name="func")
main.manager.add_update(update1)
main.manager.add_update(update2)


