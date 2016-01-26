#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
from pymoult.highlevel.updates import EagerConversionUpdate
from pymoult.highlevel.managers import ThreadedManager
import sys

main = sys.modules["__main__"]

class Data_v2(object):
    def __init__(self,value,origin="localhost"):
        self.value = value
        self.origin = origin
    def __str__(self):
        return str(self.value)+" from "+str(self.origin)

def transformer(d):
    d.origin = "localhost"

def sum_v2(d1,d2):
    return Data_v2(d1.value+d2.value,d1.origin)


manager = ThreadedManager()
manager.start()
update1 = EagerConversionUpdate(main.Data,Data_v2,transformer,module=main)
update2 = SafeRedefineUpdate(main,main.sum,sum_v2)

manager.add_update(update1)
manager.add_update(update2)

