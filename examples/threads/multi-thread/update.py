#parsed

import sys
from pymoult.stack.high_level import *
from pymoult.common.high_level import *
import time


def travel4(a,b):
	a.release()
	time.sleep(8)
	b.acquire()

def travel5(a,b):
	a.release()
	time.sleep(5)
	b.acquire()

def travel6(a,b):
	a.release()
	time.sleep(9)
	b.acquire()



t1 = get_thread_by_name("thread1")
t2 = get_thread_by_name("thread2")
t3 = get_thread_by_name("thread3")
l = [t1,t2,t3]

safe_redefine("travel1",travel4,"__main__",l)
safe_redefine("travel2",travel5,"__main__",l)
safe_redefine("travel3",travel6,"__main__",l)

