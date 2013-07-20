#parsed

import sys
from pymoult.threads import *
from pymoult.stack.high_level import *
from pymoult.common.high_level import *

def new_echo2(thread):
	print("This is thread "+str(thread)+" in 3rd version") 

t1 = get_thread_by_name("thread1")
t2 = get_thread_by_name("thread2")
t3 = get_thread_by_name("thread3")

safe_redefine("echo",new_echo2,"__main__",[t1,t2,t3])

