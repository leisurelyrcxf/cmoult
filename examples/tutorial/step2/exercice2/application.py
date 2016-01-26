#/usr/bin/python-dsu3

from pymoult.highlevel.listener import Listener
import time
import random

class Integer(object):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Serie(object):
    def __init__(self,integers):
        self.integers = integers

    def __str__(self):
        return str([str(x) for x in self.integers])


def main():
    ints=[Integer(x) for x in range(10000)]
    series = []
    while True:
        time.sleep(2)
        s = Serie([random.choice(ints) for i in range(5)])
        series.append(s)
        print([str(x) for x in series])

listener = Listener()
listener.start()
main()
