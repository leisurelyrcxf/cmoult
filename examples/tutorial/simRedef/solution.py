#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate,Update,isApplied
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
        main.shared_lock.acquire()
        time.sleep(1)
        print("Value of shared : "+str(main.shared))
        main.shared_lock.release()



def interm_writer():
    if update:
        write_shared2()
    else:
        main.shared_lock.acquire()
        time.sleep(1)
        main.shared = random.randint(0,10)
        main.shared_lock.release()



#We change read_shared and write_shared to the intermediary functions

update_reader1 = SafeRedefineUpdate(main,main.read_shared,interm_reader,name="update_reader1")
update_reader1.set_sleep_time(0.01)
update_writer1 = SafeRedefineUpdate(main,main.write_shared,interm_writer,name="update_writer1")
update_writer1.set_sleep_time(0.01)

main.manager.add_update(update_reader1)
main.manager.add_update(update_writer1)

# Now that all intermediary are in place, we trigger the update

class DataUpdate(Update):
    def check_requirements(self):
        return isApplied("update_reader1") and isApplied("update_writer1")

    def wait_alterability(self):
        main.shared_lock.acquire()
        return True

    def apply(self):
        global update
        main.shared = ["undefined time",main.shared]
        update = True

    def preresume_setup(self):
        main.shared_lock.release()


data_update = DataUpdate()
main.manager.add_update(data_update)

#Now we go change to the updated version of the functions

update_reader2 = SafeRedefineUpdate(main,main.read_shared,read_shared2,name="update_reader2")
update_reader2.set_sleep_time(0.01)
update_writer2 = SafeRedefineUpdate(main,main.write_shared,write_shared2,name="update_writer")
update_writer2.set_sleep_time(0.01)


main.manager.add_update(update_reader2)
main.manager.add_update(update_writer2)




                            




                            
