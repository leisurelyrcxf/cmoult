#!/usr/bin/pypy
from pymoult.threads import *
from pymoult.controller import *
import time

t = None

class C(object):
	def __init__(self,a,b):
		self.a = a
		self.b = b
		self.trace = []

	def display(self):
		print(self.trace)

	def addup(self):
		self.trace.append(self.a)
		self.a += self.b


def main():

	l = []
	for i in range(4):
		print("i : "+str(i))
		l.append(C(0,i))
		l[-1].display()
		l[-1].addup()
		print("added up")
		l[-1].display()
		time.sleep(5)

	for c in l:
		c.addup()
		print("next")
		c.display()
		time.sleep(5)




t = DSU_Thread(target=main)
t.start()
start_controller()

