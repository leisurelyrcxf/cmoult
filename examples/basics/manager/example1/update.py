#parsed

from pymoult.updates import SafeRedefineUpdate
import sys


main = sys.modules["__main__"]


def say_hi():
    print("hi")


def updater():
    main.say_hello = say_hi


update = SafeRedefineUpdate(main.manager,{main.say_hello:updater})

update.setup()
update.apply()
