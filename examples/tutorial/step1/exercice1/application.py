#/usr/bin/python-dsu3

from pymoult.highlevel.listener import Listener
import time



def hello():
    print("hello world")

def main():
    while True:
        time.sleep(2)
        hello()


listener = Listener()
listener.start()
main()
