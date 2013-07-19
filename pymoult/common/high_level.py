
import threading
import sys
from pymoult.common.low_level import * 

def get_thread_by_name(name):
	threads = threading.enumerate()
	for thread in threads:
		if thread.name == name:
			return thread
	return None

def pause_thread(thread):
	thread.pause_event = threading.Event()
	thread.pause_event.clear()
	def trace(frame,event,arg):
		thread.pause_event.wait()
		return None
	settrace_for_thread(thread,trace)

def resume_thread(thread):
	if hasattr(thread,"pause_event"):
		thread.pause_event.set()
		delattr(thread,"pause_event")
			



