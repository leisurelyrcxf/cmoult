#parsed
import sys
import pymoult.controllers
import inspect

class Node(object):
	def __init__(self, left, key, right):
		self.left = left
		self.key = key
		self.right = right

	def insert(self, s):
		if s < self.key:
			if self.left is None:
				return Node(Node(None, s, None), self.key, self.right)
			else:
				return Node(self.left.insert(s), self.key, self.right)
		elif s > self.key:
			if self.right is None:
				return Node(self.left, self.key, Node(None, s, None))
			else:
				return Node(self.left, self.key, self.right.insert(s))
		else:
			return self

	def member(self, s):
		if s < self.key:
			return self.left is not None and self.left.member(s)
		elif s > self.key:
			return self.right is not None and self.right.member(s)
		else:
			return True

class TableV2(object):
	def __init__(self, s=None, t=None):
		print "V2: init(" + str(s) + "," + str(t) + ")"
		if s is None:
			if t is None:
				self.root = None
			else:
				self.root = t.root
		elif t is None:
			self.root = Node(None, s, None)
		elif t.root is None:
			self.root = Node(None, s, None)
		else:
			self.root = t.root.insert(s)

	def member(self, s):
		print "V2: member " + str(s)
		return self.root is not None and self.root.member(s)

def convert(l):
	if l is None or l == []:
		return None
	ret = Node(None, l[0], None)
	for i in l[1:]:
		ret = ret.insert(i)
	return ret

def converttable(i):
	print 'converting1 ' + str(i)
	old = i.content
	del i.content
	i.__class__ = TableV2
	i.root = convert(old)

def tolist(n):
	if n is None:
		return []
	else:
		return tolist(n.left) + [n.key] + tolist(n.right)

def myupdate(pool, top_frame, bottom_frame):
	print("test")
	x = top_frame
	old_Table = sys.modules["__main__"].Table
	#Inspecting the stack frame by frame in order to  update objects
	#But if we are running an olde version of a method, we want the object to comply
	while x is not bottom_frame:
		try:
			x.f_globals['Table'] = TableV2
		except KeyError:
			pass
		#If we are instanciating a Table(v1) object
		if x.f_code is old_Table.__init__.func_code:
			_self = x.f_locals['self']
			_s = x.f_locals['s']
			_t = x.f_locals['t']
			try:
				del _self.content
			except AttributeError:
				pass
			_self.__class__ = TableV2
			if _s is None:
				if _t is None:
					_self.root = None
				elif type(_t) == old_Table:
					converttable(_t)
					_self.root = _t.root
				else:
					assert type(_t) == TableV2
					_self.root = _t.root
			elif _t is None:
				if _s is None:
					_self.root = None
				else:
					_self.root = Node(None, _s, None)
			elif type(_t) == old_Table:
				converttable(_t)
				if _t.root is None:
					_self.root = Node(None, _s, None)
				else:
					_self.root = _t.root.insert(_s)
			else:
				assert type(_t) == TableV2
				_self.root = _t.root
			x.f_locals['s'] = None
			x.f_locals['t'] = object()
			x.f_locals['t'].content = []
		#If we re in "member" method, we want to provide the "content" atribute to the object after updating
		elif x.f_code is old_Table.member.func_code:
			_self = x.f_locals['self']
			if type(_self) == old_Table:
				old = _self.content
				converttable(_self)
				_self.content = old
			else:
				assert type(_self) == TableV2
				_self.content = tolist(_self.root)
		#If we are not in a method, we just change objects in the locals
		else:
			for i in x.f_locals.values():
				if type(i) == old_Table:
					converttable(i)
		x = x.f_back
	#One the stack has been inspected, we convert every objects in the pool
	for ref in pool.objects:
		obj = ref()
		if type(obj) == old_Table:
			converttable(obj)
	#sys.modules["__main__"].Table = TableV2
	#sys.modules["__main__"].main.func_globals['Table'] = TableV2
	return True

l = sys.modules["__main__"].threads
pymoult.controllers.set_update_function(myupdate,l[0])
pymoult.controllers.set_update_method(pymoult.controllers.self_update,l[0])


