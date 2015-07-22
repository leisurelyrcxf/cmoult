#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.data_update import updateLocalVar
from pymoult.highlevel.listener import log
import sys

main = sys.modules["__main__"]

class MyUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        updateLocalVar(main.talk,"text","Hi!")
        
update = MyUpdate(name="locals")
main.manager.add_update(update)


