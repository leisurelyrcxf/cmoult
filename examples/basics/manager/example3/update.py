#parsed

from pymoult.updates import BasicUpdate
from pymoult.stack.tools import isFunctionInAllStack
import sys


main = sys.modules["__main__"]


def say_hi():
    print("hi")


def update():
    main.say_hello = say_hi

def alterability():
    return not isFunctionInAllStack(main.say_hello)

def is_over():
    return True


update = BasicUpdate(main.manager,alterability,update,is_over)

update.setup()
update.apply()
