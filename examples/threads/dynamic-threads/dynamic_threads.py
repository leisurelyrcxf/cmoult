#!/usr/bin/env pypy-dsu

import pymoult
from pymoult.threads import *
from pymoult.controller import *
import socket
import time


def echo(thread):
	print("This is thread "+str(thread)+" in 1st version")


def genMain(num):
	def main():
		while True:
			echo(num)
			time.sleep(2)
	return main

t1= DSU_Thread(target=genMain(1),name="thread1")
t2 = DSU_Thread(target=genMain(2),name="thread2")
start_controller()
t1.start()
t2.start()





