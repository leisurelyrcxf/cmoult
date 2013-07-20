#parsed
import sys
import pymoult
from pymoult.stack.high_level import *
from pymoult.common.high_level import *
import time

def main2():
	for x in range(4):
		print("This is the 2d version")
		time.sleep(3)
		

t = get_thread_by_name("thread1")
pymoult.stack.high_level.reboot_thread(t,main2)

