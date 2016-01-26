#parsed

from pymoult.highlevel.updates import SafeRedefineMethodUpdate
from pymoult.highlevel.updates import LazyConversionUpdate
from pymoult.highlevel.managers import ThreadedManager
import sys
import random

main = sys.modules["__main__"]

class Integer_v2(object):
    def __init__(self,value):
        self.value = 2*value
        
    def __str__(self):
        return str(self.value)

def intTransformer(i):
    i.value = 2*i.value


def serie__str__v2(serie):
    random.shuffle(serie.integers)
    return str([str(x) for x in serie.integers])


manager = ThreadedManager()
manager.start()

update1 = LazyConversionUpdate(main.Integer,Integer_v2,intTransformer)
update2 = SafeRedefineMethodUpdate(main.Serie,main.Serie.__str__,serie__str__v2)

manager.add_update(update1)
manager.add_update(update2)

