

import sys

def set_trace_for_thread(thread,trace):
	sys.settrace_for_thread(thread.ident,trace,True)






