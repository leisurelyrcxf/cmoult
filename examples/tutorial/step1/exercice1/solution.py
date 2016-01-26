#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
from pymoult.highlevel.managers import ThreadedManager
import sys

main = sys.modules["__main__"]

def hello_v2():
    print("Hello Dave")


manager = ThreadedManager()
manager.start()
update = SafeRedefineUpdate(main,main.hello,hello_v2)

manager.add_update(update)

