#parsed

import sys
from pymoult.threads import *
from pymoult.stack.high_level import *
from pymoult.common.high_level import *

def new_echo(thread):
	print("This is thread "+str(thread)+" in 2d version") 



t1 = get_thread_by_name("thread1")
t2 = get_thread_by_name("thread2")

safe_redefine("echo",new_echo,"__main__",[t1,t2])

t3 = DSU_Thread(target=sys.modules["__main__"].genMain(3),name="thread3")
t3.start()
