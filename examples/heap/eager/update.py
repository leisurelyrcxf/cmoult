#parsed
import sys
sys.path.insert(0,"pymoult/")
import pymoult
import pymoult.controllers
import pymoult.heap.tools


def myupdate(pool,x,y):
	for ref in pool.objects:
		obj = ref()
		if type(obj) == sys.modules["__main__"].C:
			obj.toto = obj.toto+1
	return True

class Cv2(object):
	def __init__(self,a,b):
		self.a = a
		self.b = b

	def __convert__(self):
		self.b = 0
	
	def f(self):
		print(self.a,self.b)


myupdate = pymoult.heap.tools.eager_class_update(sys.modules["__main__"].C,Cv2)

l = sys.modules["__main__"].threads
pymoult.controllers.set_update_function(myupdate,l[0])


