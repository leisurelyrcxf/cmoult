#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
import sys


main = sys.modules["__main__"]


def say_tic2():
    print("tic2")

def say_tac2():
    print("tac2")


update_tic = SafeRedefineUpdate(main,main.say_tic,say_tic2)
update_tac = SafeRedefineUpdate(main,main.say_tac,say_tac2)

main.manager.add_update(update_tic)
main.manager.add_update(update_tac)
