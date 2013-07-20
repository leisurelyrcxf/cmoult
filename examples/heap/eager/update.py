#parsed
import sys
sys.path.insert(0,"pymoult/")
import pymoult
from pymoult.heap.high_level import *


class Cv2(object):
	def __init__(self,a,b):
		self.a = a
		self.b = b

	def __convert__(self):
		self.b = 0
	
	def f(self):
		print(self.a,self.b)



import pymoult.collector
eager_class_update(sys.modules["__main__"].C,Cv2)
