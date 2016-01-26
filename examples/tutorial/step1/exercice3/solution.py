#parsed

from pymoult.highlevel.updates import EagerConversionUpdate
import sys

main = sys.modules["__main__"]

class Data_v2(object):
    def __init__(self,value,origin):
        self.value = value
        self.origin = origin
    def __str__(self):
        return str(self.value)+" from "+str(self.origin)


def transformer(data):
    data.origin = "localhost"


update = EagerConversionUpdate(main.Data,Data_v2,transformer,module=main)

main.manager.add_update(update)
