#parsed

import sys

main = sys.modules["__main__"]

class Data_v2(object):
    def __init__(self,value,origin="localhost"):
        self.value = value
        self.origin = origin
    def __str__(self):
        return str(self.value)+" from "+str(self.origin)

def sum_v2(d1,d2):
    return Data_v2(d1.value+d2.value,d1.origin)


