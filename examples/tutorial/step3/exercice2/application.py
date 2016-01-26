#/usr/bin/python-dsu3

from pymoult.highlevel.listener import Listener
import time

class Data(object):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return str(self.value)
    

def sum(d1,d2):
    return Data(d1.value+d2.value)

def main():
    data = [Data(1),Data(1)]
    i = 1
    while True:
        time.sleep(2)
        data.append(sum(data[i],data[i-1]))
        i+=1
        print([str(x) for x in data])


listener = Listener()
listener.start()
main()
