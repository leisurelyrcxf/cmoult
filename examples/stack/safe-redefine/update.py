#parsed
import sys
from pymoult.stack.high_level import *
import threading


def tst2():
	print "This is the 2d version"


threads = threading.enumerate()
safe_redefine("tst1",tst2,"__main__",threads)
