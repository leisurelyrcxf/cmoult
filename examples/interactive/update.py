#parsed

import sys
import os
import threading
import tempfile
import re

main = sys.modules["__main__"]

#Get all threads excepted the manager
def getAllThreads():
    threads = threading.enumerate()
    threads.remove(filter(lambda x : x.name == "pymoult",threads)[0])
    return threads

def getAllConnThreads():
    threads = []
    for t in threading.enumerate():
        if isinstance(t,main.ConnThread):
            threads.append(t)
    return threads

class Picture_V2(object):
    def __init__(self,path,name):
        self.basepath = path
        self.path = path
        self.name = name
        self.commentary = "Witty comment"

    def stream(self):
        f = open(self.path,'r')
        stream = f.read()
        f.close()
        return stream

    def comment(self,text):
        self.commentary = re.sub("'"," ",text)

    def annotate(self):
        new_file = os.path.join(tempfile.gettempdir(),os.path.basename(self.basepath)+"_anot.jpg")
        self.path = new_file
        os.system("convert "+self.basepath+" -background Plum -font Corsiva -pointsize 24 label:'"+self.commentary+"' -gravity Center -append "+self.path)

def pic_transformer(pic):
    pic.basepath = pic.path
    pic.commentary = "Witty comment"
        
helptext = "help : shows this help\nexit : disconnects\ncomment <folder> <comment>: sets commentary for pictures of folder\n<folder name> : downloads pictures from the folder\n(Available folders : "+" ".join(main.files.keys())+")\n"

        
def serve_folder_v2(self,folder):
    self.connection.sendall("serving")
    if self.connection.recv(1024).strip() == "go":
        for pic in main.files[folder]:
            pic.annotate()
            imgstream = pic.stream()
            self.connection.sendall("<img:"+str(len(imgstream))+">"+pic.name)
            if self.connection.recv(1024).strip() == "cancel":
                return
            self.connection.sendall(imgstream)
            if self.connection.recv(1024).strip() == "cancel":
                return
        self.connection.sendall("finished")
            
def do_command_v2(self,command):
    if command in main.files.keys():
        self.serve_folder(command)
    elif command == "exit":
        self.connection.sendall("terminating")
        self.connection.close()
        self.connection = None
    elif command[0:7] == "comment":
        args = command.split()
        if len(args)> 2 and args[1] in main.files.keys():
            for pic in main.files[args[1]]:
                pic.comment(" ".join(args[2:]))
            self.connection.sendall("Comment '"+" ".join(args[2:])+"' applied to folder "+args[1])
        else:
            self.connection.sendall(helptext)
    else:
        self.connection.sendall(helptext)
                                    
            
#end of update
        












