#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import waitQuiescenceOfFunction,resumeSuspendedThreads
from pymoult.lowlevel.relinking import redefineFunction
from pymoult.highlevel.managers import ThreadedManager
import sys

main = sys.modules["__main__"]


class CustomUpdate(Update):
    def wait_alterability(self):

    def resume_hook(self):

    def apply(self):

    

