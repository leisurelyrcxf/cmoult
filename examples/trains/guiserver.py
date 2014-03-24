#!/usr/bin/python

import socket
import tkinter
import PIL
import threading

hostname = socket.gethostname()
port = 31415


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

def do_command(command):
    l = command.split()
    print(l)
    if l[0] == "rail":
        for r in root.rails:
            if r.cget("text") == l[1]:
                r.configure(text = "")
        for r in root.stations:
            if l[1] in r.cget("text"):
                r.configure(text = r.cget("text").replace(l[1]+",",""))
                r.configure(text = r.cget("text").replace(","+l[1],""))
                r.configure(text = r.cget("text").replace(l[1],""))
        root.__getattribute__(l[2]).configure(text = l[1])
        
    elif l[0] == "station":
        for r in root.rails:
            if r.cget("text") == l[1]:
                r.configure(text = "")
        if l[2] == "Montparnasse":
            root.Montparnasse.configure(text=root.Montparnasse.cget("text")+","+l[1])
        if l[2] == "Est":
            root.Est.configure(text=root.Est.cget("text")+","+l[1])
        if l[2] == "Saint":
            root.Lazare.configure(text=root.Lazare.cget("text")+","+l[1])
                
        
def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((hostname,port))
    s.listen(10)
    while True:
        conn,addr = s.accept()
        data = conn.recv(999)
        print(data.decode("ascii"))
        do_command(data.decode("ascii"))
        data = ""
        conn.close()
    
listener = threading.Thread(target=main)
listener.start()
root.mainloop()















