#!/usr/bin/pypy
import pymoult
import pymoult.controllers
import time

t = None

class C(object):
	def __init__(self,a):
		self.a = a

	def f(self):
		print(self.a)


def main():
	c = C(9)
	for i in range(4):
		c.f()
		time.sleep(10)



pool = pymoult.controllers.enable_eager_object_conversion()
threads = pymoult.controllers.start_active_threads(pool,main)
pymoult.controllers.register_threads(threads)

