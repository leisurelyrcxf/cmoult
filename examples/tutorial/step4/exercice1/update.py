#parsed

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


             




                            
