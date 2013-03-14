#!/usr/bin/pypy
import sys
import pymoult
import pymoult.controllers
import time

def tst1():
	print 'This is the 1st version'

def main():
	while True:
		tst1()
		time.sleep(3)

threads = pymoult.controllers.start_active_threads(None,main)
pymoult.controllers.register_threads(threads)



