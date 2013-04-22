#!/usr/bin/pypy
import pymoult
import pymoult.controllers
import time
import threading


brest = threading.Lock()
rennes = threading.Lock()
tours = threading.Lock()
l=None

def travel1(a,b):
	a.release()
	print("train 1 travelling")
	time.sleep(15)
	b.acquire()

def travel2(a,b):
	a.release()
	print("train 2 travelling")
	time.sleep(10)
	b.acquire()
	

def travel3(a,b):
	a.release()
	print("train 3 travelling")
	time.sleep(5)
	b.acquire()

def main1():
	print("Train 1 starting in Brest")
	brest.acquire()
	for x in range(5):
		print("Train 1 Departing to Tours!")
		travel1(brest,tours)
		print("Train 1 arrived")
		time.sleep(10)
		print("Train 1 Departing to Brest!")
		travel1(tours,brest)
		print("Train 1 arrived")
		time.sleep(3)

def main2():
	print("Train 2 starting in Rennes")
	rennes.acquire()
	for x in range(5):
		print("Train 2 Departing to Brest!")
		travel2(rennes,brest)
		print("Train 2 arrived")
		time.sleep(8)
		print("Train 2 Departing to Tours!")
		travel2(brest,tours)
		print("Train 2 arrived")
		time.sleep(7)
		print("Train 2 Departing to Rennes!")
		travel2(tours,rennes)
		print("Train 2 arrived")
		time.sleep(3)


def main3():
	print("Train 3 starting in Tours")
	tours.acquire()
	for x in range(5):
		print("Train 3 Departing to Rennes!")
		travel3(tours,rennes)
		print("Train 3 arrived")
		time.sleep(3)
		print("Train 3 Departing to Brest!")
		travel2(rennes,brest)
		print("Train 3 arrived")
		time.sleep(5)
		print("Train 3 Departing to Tours!")
		travel2(brest,tours)
		print("Train 3 arrived")
		time.sleep(3)



threads = pymoult.controllers.start_active_threads(None,main1,main2,main3)	
pymoult.controllers.register_threads(threads)

