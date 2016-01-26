#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
import sys

main = sys.modules["__main__"]


def tic_v2():
    print("tic2")

def tac_v2():
    print("tac2")


update_tic = SafeRedefineUpdate(main,main.tic,tic_v2)
update_tac = SafeRedefineUpdate(main,main.tac,tac_v2)

main.manager.add_update(update_tic)
main.manager.add_update(update_tac)
