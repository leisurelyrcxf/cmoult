#parsed

from pymoult.highlevel.managers import Manager,SafeRedefineManager
from pymoult.highlevel.updates import SafeRedefineUpdate
import threading
import sys
import math
import time
import Queue

print("BEGIN STEP 1 OF UPDATE")


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

print("STEP 1 OF UPDATE OK")
print("BEGIN STEP 2 OF UPDATE") 


#We use a SafeRedefineUpdate-like to update stations and rails
class SafeRedefMethod(SafeRedefineManager):
    
    def add_function(self,method):
        self.functions.put(method)

    def thread_main(self):
        while not self.stop:
            self.invoked.wait()
            self.begin()
            while True:
                try:
                    method = self.functions.get(False)
                except Queue.Empty:
                    self.finish()
                    break
                method_updated = False
                while not method_updated:
                    if self.is_alterable(method[1]):
                        self.pause_threads()
                        tname= method[1].__name__

                        setattr(method[0],tname,method[2])
                        setattr(method[2],"__name__",tname)
                        method_updated = True
                        self.resume_threads()
                    time.sleep(self.sleepTime)

class SafeRedefMethodUpdate(SafeRedefineUpdate):
    def setup(self):
        for method in self.functions:
            self.manager.add_function(method)



station_and_rail_manager = SafeRedefMethod(getTrainThreads(),sleepTime=1)
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
function_updates=[[railClass,railClass.can_enter,new_Rail_can_enter]]

print("BEGIN SUBSTEP1")
update1 = SafeRedefMethodUpdate(station_and_rail_manager,function_updates)
update1.setup()
update1.apply()
update1.wait_update()
print("SUBSTEP1 OF STEP 2 OK")


function_updates = [[elementClass,elementClass.next,new_Element_next],[elementClass,elementClass.previous,new_Element_previous],[stationClass,stationClass.move_next,new_Station_move_next]]


print("BEGIN SUBSTEP2")
update2 = SafeRedefMethodUpdate(station_and_rail_manager,function_updates)
update2.setup()
update2.apply()
update2.wait_update()
print("SUBSTEP2 OF STEP 2 OK")

print("STEP 2 of UPDATE OK")
print("UPDATE COMPLETE")

        
