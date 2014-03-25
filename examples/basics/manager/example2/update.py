#parsed

from pymoult.updates import SafeRedefineUpdate
from pymoult.manager import SafeRedefineManager
import sys


main = sys.modules["__main__"]


def say_hi():
    print("hi")


def updater():
    main.say_hello = say_hi

manager = SafeRedefineManager([main.thread])
manager.start()

update = SafeRedefineUpdate(manager,{main.say_hello:updater})
update.setup()
update.apply()
