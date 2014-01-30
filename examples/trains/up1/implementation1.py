#parsed

#First implementation : 
#Update of Train by Mixin 
#Update of functions by 

from pymoult.manager import Manager,SafeRedefineManager
from pymoult.updates import SafeRedefineUpdate
import threading
import sys
import math

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
    threads = filter(f,threading.enumerate())
    return threads
#The following class is specific for this update, therefore it comes with the code for the update, it also plays the role of an Update class
#
class TrainManager(Manager):
    def __init__(self):
        train_threads = getTrainThreads()
        super(TrainManager,self).__init__(threads=train_threads)

    
    def start(self):
        #Adding a direction field for each train
        for train in self.threads:
            train.direction = "right"
        #Updating the constructor and adding a method
        sys.modules["__main__"].Train.__init__ = newTrainInit
        sys.modules["__main__"].Train.switch_direction = switch_direction


manager1 = TrainManager()
manager1.start()

#We use the SafeRedefineUpdate to update stations and rails
station_and_rail_manager = SafeRedefineManager(getTrainThreads(),sleepTime=3)
station_and_rail_manager.start()

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





def generate_updater(function,clas,target):
    def f():
        setattr(clas,function,target)
    return f


functions_updates = {elementClass.next:generate_updater("next",elementClass,new_Element_next),elementClass.previous:generate_updater("previous",elementClass,new_Element_previous),railClass.can_enter:generate_updater("can_enter",railClass,new_Rail_can_enter),stationClass.move_next:generate_updater("move_next",stationClass,new_Station_move_next)}

update1 = SafeRedefineUpdate(station_and_rail_manager,functions_updates)
update1.setup()
update1.apply()



 

        
