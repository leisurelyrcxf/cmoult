#parsed

from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.updates import Update
from pymoult.lowlevel.alterability import waitQuiescenceOfFunction
from pymoult.lowlevel.data_update import addMethodToClass
import threading
import sys
import math
import time
import queue


main = sys.modules["__main__"]

def newTrainInit(self,speed,color,position,direction):
    train.color = color
    train.speed = speed
    train.position = position
    train.direction = direction
    super(Train,self).__init__(target=self.main,name=self.color+"_train")

def switch_direction(self):
    if self.direction == "right":
        self.direction = "left"
    else:
        self.direction = "right"
    sys.modules["__main__"].gprint("The "+self.color+" train is changing direction to "+self.direction)

def getTrainThreads():
    def f(t):
        if t.name in ["blue_train","red_train","green_train","purple_train","orange_train","white_train"]:
            return True
        else:
            return False
           
    #We can get all the train through the enumerate method
    threads = list(filter(f,threading.enumerate()))
    return threads


manager = ThreadedManager(name="GlobalManager",threads=getTrainThreads())
manager.start()

class TrainUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        for train in self.manager.threads:
            train.direction = "right"
        addMethodToClass(main.Train,"__int__",newTrainInit)
        addMethodToClass(main.Train,"switch_direction",switch_direction)
    def cleanup(self):
        print("Trains sucessfully updated")

manager.add_update(TrainUpdate(name="Trains"))

class SafeMethodUpdate(Update):
    def __init__(self,cls,method,nmethod,name=None):
        self.cls = cls
        self.method = method
        self.nmethod = nmethod
        super(SafeMethodUpdate,self).__init__(name=name)
    def wait_alterability(self):
        return waitQuiescenceOfFunction(self.method)
    def apply(self):
        addMethodToClass(self.cls,self.method.__name__,self.nmethod)
    def cleanup(self):
        print("Method "+self.method.__name__+" of class "+self.cls.__name__+" updated")
        return True

railClass = sys.modules["__main__"].Rail
elementClass = sys.modules["__main__"].Element
stationClass = sys.modules["__main__"].Station


def new_Element_next(self,train):
    if train.direction == "right":
        return self.right
    else:
        return self.left

def new_Element_previous(self,train):
    if train.direction == "right":
        return self.left
    else:
        return self.right

def new_Rail_can_enter(self,train):
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
        if isinstance(nextRail,stationClass):
            #We have reached the end of the railroad
            #We check if all trains met plus our train can stay in this station
            ans = nextRail.can_enter(pending)
            self.lane.condition.release()
            return ans
        else:
            #Next Rail section
            if nextRail.train != None:
                pending+=1
                if nextRail.train.direction != train.direction:
                    self.lane.condition.release()
                    return False
            if previousTrain == None and nextRail.train != None:
                #We have to compare to the first train met only
                previousTrain = nextRail.train
            if previousTrain != None:
                #The previous train must leave the next rail section before we reach the end of this rail
                if not (math.ceil(rail.length/train.speed) > math.ceil(nextRail.length/previousTrain.speed)):
                    self.lane.condition.release()
                    return False
        rail = nextRail
                                

def new_Station_move_next(self,train):
    lane = None
    if train.direction == "right":
        lane = self.rightLane
        if lane == None:
            train.switch_direction()
            lane = self.leftLane
    else:
        lane = self.leftLane
        if lane == None:
            train.switch_direction()
            lane = self.rightLane
    lane.condition.acquire()
    nextElement = self.next(train)
    if nextElement == None:
        lane.condition.release()
        return self
    while not nextElement.can_enter(train):
        lane.condition.wait()
    self.removeTrain()
    if nextElement.train == None:
        nextElement.train = train
    else:
        raise Exception("Error at Station "+self.name+" ! the "+train.color+" could not enter next rail!")
    lane.condition.notifyAll()
    lane.condition.release()
    return nextElement

#We need to update Rail.can_enter before allowing for trains to switch direction
#If we don't, the old version of Rail.can_enter may be executed and allow an accident!!

railUpdate = SafeMethodUpdate(railClass,railClass.can_enter,new_Rail_can_enter,name="Rail")
manager.add_update(railUpdate)

elementUpdate1 = SafeMethodUpdate(elementClass,elementClass.next,new_Element_next,name="Element1")
manager.add_update(elementUpdate1)
elementUpdate2 = SafeMethodUpdate(elementClass,elementClass.previous,new_Element_previous,name="Element2")
manager.add_update(elementUpdate2)
stationUpdate = SafeMethodUpdate(stationClass,stationClass.move_next,new_Station_move_next,"Station")
manager.add_update(stationUpdate)


        
