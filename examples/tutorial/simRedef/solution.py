#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate
from pymoult.lowlevel.stack import suspendThread,resumeThread
import random
import sys
import time

main = sys.modules["__main__"]

def read_shared2():
    main.shared_lock.acquire()
    time.sleep(2)
    print("Value of shared at "+main.shared[0]+" : "+str(main.shared[1]))
    main.shared_lock.release()

def write_shared2():
    main.shared_lock.acquire()
    time.sleep(2)
    main.shared = [time.strftime("%H:%M:%S"),random.randint(0,10)]
    main.shared_lock.release()    

#Do deal with this update we use the strategy implemnted in DynamOS
#See "Dynamic and Adaptive Updates of Non-Quiescent Subsystems in Commodity Operating System Kernels"
#in proceedings of Eurosys 2007 for more details.
#First, we want to define intermediary functions for updating read_shared and write_shared

update = False 

def interm_reader():
    if update:
        read_shared2()
    else:
        main.read_shared()

def interm_writer():
    if update:
        write_shared2()
    else:
        main.write_shared2()

#We change read_shared and write_shared to the intermediary functions

print("Begining Step 1")

update = SafeRedefineUpdate(main.manager,{main.read_shared:[main,interm_reader],main.write_shared:[main,interm_writer]})

update.setup()
update.apply()
update.wait_update()

# Now that all intermediary are in place, we trigger the update

print("Begining Step 2")
#Suspend threads
suspendThread(main.reader)
suspendThread(main.writer)
#Update the shared variable
main.shared = ["undefined time",main.shared]
#trigger the new version of the functions
update = True
#resume the threads
resumeThread(main.reader)
resumeThread(main.writer)

print("Begining Step 3")
#Now we go change to the updated version of the functions
update = SafeRedefineUpdate(main.manager,{main.read_shared:[main,read_shared2],main.write_shared:[main,write_shared2]})

update.setup()
update.apply()
update.wait_update()

print("END OF UPDATE")



                            




                            
