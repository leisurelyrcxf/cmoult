#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
import sys


main = sys.modules["__main__"]


def say_tic2():
    print("tic2")

def say_tac2():
    print("tac2")


update = SafeRedefineUpdate(main.manager,{main.say_tic:[main,say_tic2],main.say_tac:[main,say_tac2]})

update.setup()
update.apply()
update.wait_update()

print("update complete")
