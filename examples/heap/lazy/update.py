#parsed
import sys
sys.path.insert(0,"pymoult/")
import pymoult.heap.tools
import time

t = None

class Cv2(object):
	def __init__(self,a,b):
		self.a = a + b
		self.b = 8
		self.trace = {}
	
	def __convert__(self):
		self.trace = {}


	def display(self):
		print(self.trace)

	def addup(self):
		self.trace[self.a] = self.a + self.b
		self.a += self.b
		

pymoult.heap.tools.start_lazy_update_class(sys.modules["__main__"].C,Cv2)
