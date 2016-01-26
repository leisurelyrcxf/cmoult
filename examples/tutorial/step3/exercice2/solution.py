#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import waitQuiescenceOfFunction,resumeSuspendedThreads
from pymoult.lowlevel.relinking import redefineFunction
from pymoult.lowlevel.data_access import DataAccessor
from pymoult.lowlevel.data_update import redefineClass,updateToClass
from pymoult.highlevel.managers import ThreadedManager
import sys

main = sys.modules["__main__"]

class Data_v2(object):
    def __init__(self,value,origin):
        self.value = value
        self.origin = origin
    def __str__(self):
        return str(self.value)+" from "+str(self.origin)

def transformer(d):
    d.origin = "localhost"

def sum_v2(d1,d2):
    return Data_v2(d1.value+d2.value,d1.origin)

class CustomUpdate(Update):
    def wait_alterability(self):
        return waitQuiescenceOfFunction(main.sum)

    def apply(self):
        redefineFunction(main,main.sum,sum_v2)
        all_data = DataAccessor(main.Data,"immediate")
        for d in all_data:
            updateToClass(d,main.Data,Data_v2,transformer)
        redefineClass(main,main.Data,Data_v2)
    def resume_hook(self):
        resumeSuspendedThreads()







manager = ThreadedManager()
manager.start()
update = CustomUpdate()

manager.add_update(update)

