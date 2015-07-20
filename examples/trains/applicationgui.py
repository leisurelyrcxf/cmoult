#!/usr/bin/python-dsu3

from pymoult.highlevel.listener import Listener

import math
import time
import threading
import tkinter
import threading


#GUI

class Window(tkinter.Tk):
    def __init__(self):
        super(Window,self).__init__()
        self.setup()
        self.resizable(True,True)
        self.configure(background="white")
        self.geometry("800x600+0+0")
        self.title("Reconfigurable trains!")

    def setup(self):
        self.grid()
        self.mpl = tkinter.Label(self,font=("Sans",14),text="Montparnasse",fg="black",bg="white")
        self.mpl.grid(row=0,column=1)
        self.el = tkinter.Label(self,font=("Sans",14),text="Est",fg="black",bg="white")
        self.el.grid(row=0,column=5)
        self.sll = tkinter.Label(self,font=("Sans",14),text="Saint Lazare",fg="black",bg="white")
        self.sll.grid(row=4,column=1)
        self.rail0 = tkinter.Canvas(self,width=100,height=20,bg="white")
        self.rail0.grid(row=1,column=2)
        self.rail0.create_line(0,10,100,10)
        self.rail1 = tkinter.Canvas(self,width=40,height=20,bg="white")
        self.rail1.grid(row=1,column=3)
        self.rail1.create_line(0,10,40,10)
        self.rail2 = tkinter.Canvas(self,width=160,height=20,bg="white")
        self.rail2.grid(row=1,column=4)
        self.rail2.create_line(0,10,160,10)
        self.rail3 = tkinter.Canvas(self,width=20,height=200,bg="white")
        self.rail3.grid(row=2,column=5)
        self.rail3.create_line(10,0,10,200)
        self.rail4 = tkinter.Canvas(self,width=120,height=20,bg="white")
        self.rail4.grid(row=3,column=2,columnspan=3)
        self.rail4.create_line(0,10,120,10)
        self.rail5 = tkinter.Canvas(self,width=20,height=300,bg="white")
        self.rail5.grid(row=2,column=1)
        self.rail5.create_line(10,0,10,300,fill="red")
        self.ME1 = tkinter.Label(self,font=("Sans",16),text="",fg="black",bg="white")
        self.ME1.grid(row=0,column=2)
        self.ME2 = tkinter.Label(self,font=("Sans",16),text="",fg="black",bg="white")
        self.ME2.grid(row=0,column=3)
        self.ME3 = tkinter.Label(self,font=("Sans",16),text="",fg="black",bg="white")
        self.ME3.grid(row=0,column=4)
        self.ESL1 = tkinter.Label(self,font=("Sans",16),text="",fg="black",bg="white")
        self.ESL1.grid(row=2,column=6)
        self.ESL2 = tkinter.Label(self,font=("Sans",16),text="",fg="black",bg="white")
        self.ESL2.grid(row=4,column=2,columnspan=3)
        self.SLM1 = tkinter.Label(self,font=("Sans",16),text="",fg="black",bg="white")
        self.SLM1.grid(row=2,column=0)
        self.Montparnasse = tkinter.Label(self,font=("Sans",16),text="blue,red,orange,white",fg="black",bg="white")
        self.Montparnasse.grid(row=1,column=1)
        self.Est = tkinter.Label(self,font=("Sans",16),text="green,purple",fg="black",bg="white")
        self.Est.grid(row=1,column=5)
        self.Lazare = tkinter.Label(self,font=("Sans",16),text="",fg="black",bg="white")
        self.Lazare.grid(row=3,column=1)
        self.rails = [self.ME1,self.ME2,self.ME3,self.ESL1,self.ESL2,self.SLM1]
        self.stations = [self.Montparnasse,self.Est,self.Lazare]

root = Window()


#END GUI







lock = threading.Lock()

def gprint(string):
    lock.acquire()
    print(string)
    lock.release()


class Train(threading.Thread):
    def __init__(self,speed,color,position):
        self.color = color
        self.speed = speed
        self.position = position
        self.stoped = False
        super(Train,self).__init__(name=self.color+"_train")

    def move(self):
        if type(self.position) == Station:
            time.sleep(3)
            gprint("The "+self.color+" train wants to leave the "+self.position.name+" station")
            oldpos = self.position.name
            self.position = self.position.move_next(self)
            gprint("The "+self.color+" train entered on the "+self.position.name+" rail")
            if isinstance(self.position,Rail):
                s = root.__getattribute__(oldpos.replace("Saint Lazare","Lazare"))
                s.configure(text = s.cget("text").replace(self.color+",",""))
                s.configure(text = s.cget("text").replace(","+self.color,""))
                s.configure(text = s.cget("text").replace(self.color,""))
                root.__getattribute__(self.position.name).configure(text=self.color)
        elif type(self.position) == Rail:
            time.sleep(math.ceil(self.position.length/self.speed))
            oldpos = self.position.name
            r = root.__getattribute__(oldpos)
            self.position = self.position.move_next()
            n = root.__getattribute__(self.position.name.replace("Saint Lazare","Lazare"))
            r.configure(text="")
            if isinstance(self.position,Station):
                gprint("The "+self.color+" train entered the "+self.position.name+" station")
                n.configure(text=n.cget("text")+","+self.color)
            else:
                gprint("The "+self.color+" train entered on the "+self.position.name+" rail")
                n.configure(text=self.color)

    def run(self):
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
 #   lane2 = Lane(lazare,rail5,montparnasse)
    lane0.link()
    lane1.link()
 #   lane2.link()

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

    root.mainloop()
    
listener = Listener()
listener.start()
main()
    
        
