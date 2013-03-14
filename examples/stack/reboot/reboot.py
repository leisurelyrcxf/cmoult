#!/usr/bin/pypy
import sys
import pymoult
import pymoult.controllers
import time



def main():
	for x in range(4):
		print("this is the 1st version")
		time.sleep(3)

threads = pymoult.controllers.start_active_threads(None,main)
pymoult.controllers.register_threads(threads)
