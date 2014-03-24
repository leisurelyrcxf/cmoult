#parsed

from pymoult.updates import SafeRedefineUpdate
import sys


main = sys.modules["__main__"]


def say_hi():
    print("hi")


update = main.UpUpdate(say_hi)
update.setup()
update.apply()
