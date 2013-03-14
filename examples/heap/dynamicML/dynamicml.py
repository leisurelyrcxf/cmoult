#!/usr/bin/pypy
import sys
import pymoult
import pymoult.controllers
import time
import inspect

class Table(object):
	def __init__(self, s=None, t=None):
		print "V1: init(" + str(s) + "," + str(t) + ")"
		if s is None:
			if t is None:
				self.content = []
			else:
				self.content = t.content
		elif t is None:
			self.content = [s]
		else:
			self.content = [s] + t.content

	def member(self, s):
		print "V1: member " + str(s)
		return self.content is not None and s in self.content

t = None

def main():
	keys = ['toto', 'titi', 'tutu', 'tata', 'tete', 'tyty']
	c = Table()
	for i in keys:
		c = Table(i, c)
		time.sleep(1)
	tests = ['foto', 'titi', 'zutu', 'tada', 'tete', 'tyty']
	time.sleep(10)
	for i in tests:
		print c.member(i)
		time.sleep(1)
	print("finished")

pool = pymoult.controllers.enable_eager_object_conversion()
threads = pymoult.controllers.start_active_threads(pool,main)
pymoult.controllers.register_threads(threads)


