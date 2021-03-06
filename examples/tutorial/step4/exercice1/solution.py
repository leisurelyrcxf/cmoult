#parsed

from pymoult.highlevel.updates import SafeRedefineUpdate,Update,isApplied
import random
import sys
import time

main = sys.modules["__main__"]

def read_shared2():
    main.shared_lock.acquire()
    time.sleep(1)
    print("Value of shared at "+main.shared[0]+" : "+str(main.shared[1]))
    main.shared_lock.release()


def write_shared2():
    main.shared_lock.acquire()
    time.sleep(1)
    main.shared = [time.strftime("%H:%M:%S"),random.randint(0,10)]
    main.shared_lock.release()

update = False 

def interm_reader():
    main.shared_lock.acquire()
    time.sleep(1)
    if update:
        #Code of read_shared2
        print("Value of shared at "+main.shared[0]+" : "+str(main.shared[1]))
    else:
        #Code of read_shared1
        print("Value of shared : "+str(main.shared))
    main.shared_lock.release()

def interm_writer():
    main.shared_lock.acquire()
    if update:
        #code of write_shared2
        main.shared = [time.strftime("%H:%M:%S"),random.randint(0,10)]
    else:
        #code of write_shared1
        main.shared = random.randint(0,10)
    main.shared_lock.release()



update_reader1 = SafeRedefineUpdate(main,main.read_shared,interm_reader,name="update_reader1")
update_reader1.set_sleep_time(0.1)
update_writer1 = SafeRedefineUpdate(main,main.write_shared,interm_writer,name="update_writer1")
update_writer1.set_sleep_time(0.1)

main.manager.add_update(update_reader1)
main.manager.add_update(update_writer1)

class DataUpdate(Update):
    def check_requirements(self):
        if isApplied("update_reader1") and isApplied("update_writer1"):
            return "yes"
        else:
            return "no"

    def wait_alterability(self):
        main.shared_lock.acquire()
        return True

    def apply(self):
        global update
        main.shared = ["undefined time",main.shared]
        update = True

    def preresume_setup(self):
        main.shared_lock.release()


data_update = DataUpdate(name="data")
main.manager.add_update(data_update)

class SecondUpdate(SafeRedefineUpdate):
    def check_requirements(self):
        if isApplied("data"):
            return "yes"
        else:
            return "no"


update_reader2 = SecondUpdate(main,main.read_shared,read_shared2,name="update_reader2")
update_reader2.set_sleep_time(0.1)
update_writer2 = SecondUpdate(main,main.write_shared,write_shared2,name="update_writer2")
update_writer2.set_sleep_time(0.1)

main.manager.add_update(update_reader2)
main.manager.add_update(update_writer2)




                            




                            
