#!/usr/bin/pypy-dsu
from pymoult.collector import *
from pymoult.controller import *
from pymoult.threads import * 
import time

t = None

class C(object):
	def __init__(self,a):
		self.a = a

	def f(self):
		print(self.a)


def main():
	print("coucou")
	c = C(9)
	for i in range(4):
		c.f()
		time.sleep(10)


enable_pool()
start_controller()
t = DSU_Thread(target=main)
t.start()
