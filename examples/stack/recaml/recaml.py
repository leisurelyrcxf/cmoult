#!/usr/bin/pypy
import pymoult
import pymoult.controllers

# lasti -1: call
def fib(n):
# lasti 0
	if n <= 1:
# lasti 12
		return n
# lasti 15: return from fib (then)
	else:
# lasti 16
		x = fib(n-2)
# lasti 26: return from fib(n-2)
# lasti 32
		y = fib(n-1)
# lasti 42: return from fib(n-1)
# lasti 48
		return x+y
# lasti 55: return from fib (else)

# lasti -1: call
def main():
# lasti 0
	print("Starting iterative calculation of fib(1234)")
	x = fib(1234)
# lasti 6: return from fib(1234)
# lasti 12
	print x
# lasti: return from main ???


threads = pymoult.controllers.start_active_threads(None,main)
pymoult.controllers.register_threads(threads)
