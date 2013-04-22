#!/usr/bin/env pypy

import pymoult
import pymoult.controllers
import socket
import time


def echo(thread):
	print("This is thread "+str(thread)+" in 1st version")


def genMain(num):
	def main():
		while True:
			echo(num)
			time.sleep(2)
	return main

threads = pymoult.controllers.start_active_threads(None,genMain(1),genMain(2))
pymoult.controllers.register_threads(threads)






