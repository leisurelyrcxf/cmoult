#!/usr/bin/pypy-dsu
import sys
import pymoult
from pymoult.controller import *
from pymoult.threads import *
import time



def main():
	for x in range(4):
		print("this is the 1st version")
		time.sleep(3)

t = DSU_Thread(target=main,name="thread1")
start_controller()
t.start()
