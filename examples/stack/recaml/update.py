#parsed
import pymoult.controllers
import sys
import threading

def merge2(nn,fibnn,bestn_1,bestfibn_1):
	if bestn_1 is None:
		return (nn,fibnn,None,None,None,None)
	elif bestn_1 == nn-1:
		if bestfibn_1 is None:
			return (nn,fibnn,None,None,None,None)
		else:
			return (nn,fibnn,nn,fibnn,bestn_1,bestfibn_1)
	else:
		return (nn,fibnn,None,None,None,None)
def merge1(nn,fibnn,bestn,bestfibn,bestn_1,bestfibn_1):
	if bestn is None:
		return merge2(nn,fibnn,bestn_1,bestfibn_1)
	elif bestn == nn-1:
		if bestfibn is None:
			return merge2(nn,fibnn,bestn_1,bestfibn_1)
		else:
			return (nn,fibnn,nn,fibnn,bestn,bestfibn)
	else:
		return (nn,fibnn,bestn,bestfibn,bestn_1,bestfibn_1)
def merge(n,fibn,nn,fibnn,bestn,bestfibn,bestn_1,bestfibn_1):
	if nn is not None and fibnn is not None:
		print "found fib(" + str(nn) + ")=" + str(fibnn)
	if fibnn is None:
		return (n,fibn,bestn,bestfibn,bestn_1,bestfibn_1)
	elif n is None:
		return merge1(nn,fibnn,bestn,bestfibn,bestn_1,bestfibn_1)
	elif n == nn-1:
		if fibn is None:
			return merge1(nn,fibnn,bestn,bestfibn,bestn_1,bestfibn_1)
		else:
			return (nn,fibnn,nn,fibnn,n,fibn)
	else:
		return (nn,fibnn,bestn,bestfibn,bestn_1,bestfibn_1)

def new(m, n, fibn, fibn_1):
	if n is None or fibn is None or fibn_1 is None:
		if m == 0:
			print m
			return
		else:
			i, fibi, fibi_1 = (1, 1, 0)
	else:
		print "restart at " + str(n)
		(i, fibi, fibi_1) = (n, fibn, fibn_1)
	while i < m:
		(i, fibi, fibi_1) = (i+1, fibi+fibi_1, fibi)
	print fibi

def update_fib(pool, topframe,bottomframe):
	thread = threading.current_thread()
	x = topframe
	a = thread.trace_arg
	maxn = None
	n = None
	fibn = None
	bestn = None
	bestfibn = None
	bestn_1 = None
	bestfibn_1 = None
	fib = sys.modules['__main__'].fib
	main = sys.modules['__main__'].main
	print str([main, fib])
	while x is not bottomframe:
		if x.f_code is fib.func_code:
			nn = x.f_locals['n']
			maxn = max(maxn, nn)
			if x.f_lasti == -1:
				pass
			elif x.f_lasti == 0:
				pass
			elif x.f_lasti == 12:
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn,nn,bestn,bestfibn,bestn_1,bestfibn_1)
			elif x.f_lasti == 15:
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn,nn,bestn,bestfibn,bestn_1,bestfibn_1)
			elif x.f_lasti == 16:
				pass
			elif x.f_lasti == 26:
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-2,a,bestn,bestfibn,bestn_1,bestfibn_1)
			elif x.f_lasti == 32:
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-2,x.f_locals['x'],bestn,bestfibn,bestn_1,bestfibn_1)
			elif x.f_lasti == 42:
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-2,x.f_locals['x'],bestn,bestfibn,bestn_1,bestfibn_1)
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-1,a,bestn,bestfibn,bestn_1,bestfibn_1)
			elif x.f_lasti == 48:
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-2,x.f_locals['x'],bestn,bestfibn,bestn_1,bestfibn_1)
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-1,x.f_locals['y'],bestn,bestfibn,bestn_1,bestfibn_1)
			elif x.f_lasti == 55:
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-2,x.f_locals['x'],bestn,bestfibn,bestn_1,bestfibn_1)
				(n,fibn,bestn,bestfibn,bestn_1,bestfibn_1) = merge(n,fibn,nn-1,x.f_locals['y'],bestn,bestfibn,bestn_1,bestfibn_1)
			else:
				print 'Hum... unknown x.f_lasti ' + str(x.f_lasti)
		elif x.f_code is main.func_code:
			new(maxn, bestn, bestfibn, bestfibn_1)
			exit()
		else:
			print 'Hum... unknown code object ' + str(x.f_code)
		x = x.f_back
		a = None
	print 'Hum... embarrassing...'
	assert False
	exit()

l = sys.modules["__main__"].threads
pymoult.controllers.set_update_function(update_fib,l[0])

