#parsed

from pymoult.highlevel.managers import ThreadedManager
import sys

main = sys.modules["__main__"]

manager = ThreadedManager()
manager.start()


