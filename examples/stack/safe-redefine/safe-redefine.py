#!/usr/bin/pypy
import sys
import pymoult
from pymoult.threads import *
from pymoult.controller import *
import time

def tst1():
	print 'This is the 1st version'

def main():
	while True:
		tst1()
		time.sleep(3)

t = DSU_Thread(target=main)
start_controller()
t.start()



