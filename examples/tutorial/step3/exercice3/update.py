#parsed

from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import waitStaticPoints,setupWaitStaticPoints,cleanFailedStaticPoints,resumeSuspendedThreads
import sys

main = sys.modules["__main__"]


def tic_v2():
    print("tic2")

def tac_v2():
    print("tac2")


class CustomUpdate(Update):
    def preupdate_setup(self):


    def wait_alterability(self):


    def apply(self):


    def resume_hook(self):

        
    def clean_failed_alterability(self):


    
update = CustomUpdate()
main.manager.add_update(update)

