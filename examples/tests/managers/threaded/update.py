#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
from pymoult.highlevel.listener import log
import sys

main = sys.modules["__main__"]

def func_v2():
    log(0,"v2")

update = SafeRedefineUpdate(main,main.func_v1,func_v2,name="func")
main.manager.add_update(update)


