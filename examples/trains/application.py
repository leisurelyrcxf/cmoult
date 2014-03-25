#!/usr/bin/pypy-dsu

from pymoult.threads import DSU_Thread
from pymoult.listener import Listener


import math
import time
import threading


lock = threading.Lock()

def gprint(string):
    lock.acquire()
    print(string)
    lock.release()


class Train(DSU_Thread):
    def __init__(self,speed,color,position):
        self.color = color
        self.speed = speed
        self.position = position
        
        super(Train,self).__init__(target=self.main,name=self.color+"_train")
        
    def move(self):
        if type(self.position) == Station:
            time.sleep(3)
            gprint("The "+self.color+" train wants to leave the "+self.position.name+" station")
            self.position = self.position.move_next(self)
            gprint("The "+self.color+" train entered on the "+self.position.name+" rail")
        elif type(self.position) == Rail:
            time.sleep(math.ceil(self.position.length/self.speed))
            self.position = self.position.move_next()
            if isinstance(self.position,Station):
                gprint("The "+self.color+" train entered the "+self.position.name+" station")
            else:
                gprint("The "+self.color+" train entered on the "+self.position.name+" rail")


    def main(self):
        while not self.stoped:
            self.move()
    
               
class Element(object):
    def __init__(self,name,left=None,right=None):
        self.left = left
        self.right = right
        self.name = name
    
    def move_next(self,train):
        pass
 
    def next(self,train):
        return self.right

    def previous(self,train):
        return self.left
        

class Lane(object):
    def __init__(self,*elements):
        self.elements = elements
        self.condition = threading.Condition()
        self.elements[0].rightLane = self
        self.elements[len(self.elements)-1].leftLane = self
        for i in range(1,len(self.elements)-1):
            self.elements[i].lane = self


    def link(self):
        n = len(self.elements)
        self.elements[0].right = self.elements[1]
        self.elements[n-1].left = self.elements[n-2]
        for i in range(1,n-1):
            self.elements[i].right = self.elements[i+1]
            self.elements[i].left = self.elements[i-1]

    
class Station(Element):
    def __init__(self,name,maxTrain,left=None,right=None):
        super(Station,self).__init__(name,left,right)
        self.maxTrain = maxTrain
        self.nTrain = 0
        self.rightLane = None
        self.leftLane = None
        self.lock = threading.Lock()
        
    def addTrain(self):
        self.lock.acquire()
        self.nTrain += 1
        self.lock.release()

    def removeTrain(self):
        self.lock.acquire()
        self.nTrain -= 1
        self.lock.release()

    def move_next(self,train):
        if self.rightLane == None:
            return self
        self.rightLane.condition.acquire()
        nextElement = self.next(train)
        while not nextElement.can_enter(train):
            self.rightLane.condition.wait()
        self.removeTrain()
        if nextElement.train == None:
            nextElement.train = train
        else:
            raise Exception("Error at Station "+self.name+" ! the "+train.color+" could not enter next rail!")
        self.rightLane.condition.notifyAll()
        self.rightLane.condition.release()
        return nextElement

    def can_enter(self,pending):
        return ((self.nTrain+pending) < self.maxTrain)
        


class Rail(Element):
    def __init__(self,name,length,left=None,right=None):
        super(Rail,self).__init__(name,left,right)
        self.length = length
        self.hasTrain = False
        self.condition = threading.Condition()
        self.train = None
        self.lane = None

    def move_next(self):
        self.lane.condition.acquire()
        nextElement = self.next(self.train)
        if isinstance(nextElement,Station):
            nextElement.addTrain()
        if isinstance(nextElement,Rail):
            if nextElement.train == None:
                nextElement.train = self.train
            else:
                raise Exception("Error at rail "+self.name+" ! the "+self.train.color+" could not enter next rail!")
        self.train = None
        self.lane.condition.notifyAll()
        self.lane.condition.release()
        return nextElement
   
    def can_enter(self,train):
        self.lane.condition.acquire()
        previousTrain = None
        rail = self
        pending = 0 
        #If this rail already has a train, we return False
        if self.train != None:
            self.lane.condition.release()
            return False
        #We run along the rail
        while True:
            nextRail = rail.next(train)
            if isinstance(nextRail,Station):
                #We have reached the end of the railroad
                #We check if all trains met plus our train can stay in this station
                ans = nextRail.can_enter(pending)
                self.lane.condition.release()
                return ans
            else:
                #Next Rail section
                if nextRail.train != None:
                    pending+=1
                if previousTrain == None and nextRail.train != None:
                    #We have to compare to the first train met only
                    previousTrain = nextRail.train
                if previousTrain != None:
                    #The previous train must leave the next rail section before we reach the end of this rail
                    if not (math.ceil(rail.length/train.speed) > math.ceil(nextRail.length/previousTrain.speed)):
                        self.lane.condition.release()
                        return False
            rail = nextRail
        


                        
def main():
    montparnasse = Station("Montparnasse",8)
    est = Station("Est",3)
    lazare = Station("Saint Lazare",6)
    rail0 = Rail("ME1",50) 
    rail1 = Rail("ME2",20)
    rail2 = Rail("ME3",80)
    rail3 = Rail("ESL1",100)
    rail4 = Rail("ESL2",60)
    rail5 = Rail("SLM1",150)
    
    lane0 = Lane(montparnasse,rail0,rail1,rail2,est)
    lane1 = Lane(est,rail3,rail4,lazare)
#    lane2 = Lane(lazare,rail5,montparnasse)
    lane0.link()
    lane1.link()
#    lane2.link()

    blueTrain = Train(30,"blue",montparnasse)
    redTrain = Train(10,"red",montparnasse)
    greenTrain = Train(40,"green",est)
    purpleTrain = Train(30,"purple",est)
    orangeTrain = Train(20,"orange",montparnasse)
    whiteTrain = Train(40,"white",montparnasse)

    blueTrain.start()
    redTrain.start()
    greenTrain.start()
    purpleTrain.start()
    orangeTrain.start()
    whiteTrain.start()



listener = Listener()
listener.start()
main()
    
        
