#parsed

import sys
import os
import threading
import tempfile
import socket
import re

main = sys.modules["__main__"]

#Get all threads excepted the manager
def getAllThreads():
    threads = threading.enumerate()
    pymoult_thread = list(filter(lambda x : x.name == "pymoult",threads))
    if len(pymoult_thread) > 0:
        threads.remove(pymoult_thread[0])
    else:
        threads.remove(threading.current_thread())
    return threads

def getAllConnThreads():
    threads = []
    for t in threading.enumerate():
        if isinstance(t,main.ConnThread):
            threads.append(t)
    if threading.current_thread() in threads:
        threads.remove(threading.current_thread())
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
        
helptext = "help : shows this help\nexit : disconnects\ncomment <folder> <comment>: sets commentary for pictures of folder\n<folder name> : downloads pictures from the folder\n(Available folders : "+" ".join(list(main.files.keys()))+")\n"

        
def serve_folder_v2(self,folder):
    try:
        self.connection.sendall("serving".encode("ascii"))
        if self.connection.recv(1024).decode("utf-8").strip() == "go":
            for pic in main.files[folder]:
                pic.annotate()
                imgstream = pic.stream()
                s = "<img:"+str(len(imgstream))+">"+pic.name
                self.connection.sendall(s.encode("ascii"))
                if self.connection.recv(1024).decode("utf-8").strip() == "cancel":
                    return
                self.connection.sendall(imgstream)
                if self.connection.recv(1024).decode("utf-8").strip() == "cancel":
                    return
            self.connection.sendall("finished".encode("ascii"))
    except socket.timeout:
        #Send finish in the client is waiting for it
        self.connection.sendall("finished".encode("ascii"))
            
def do_command_v2(self,command):
    if command in list(main.files.keys()):
        self.serve_folder(command)
    elif command == "exit":
        self.connection.sendall("terminating".encode("ascii"))
        self.connection.close()
        self.connection = None
    elif command[0:7] == "comment":
        args = command.split()
        if len(args)> 2 and args[1] in list(main.files.keys()):
            for pic in main.files[args[1]]:
                pic.comment(" ".join(args[2:]))
            s = "Comment '"+" ".join(args[2:])+"' applied to folder "+args[1]
            self.connection.sendall(s.encode("ascii"))
        else:
            self.connection.sendall(helptext.encode("ascii"))
    else:
        self.connection.sendall(helptext.encode("ascii"))
                                    
            
#end of update
        












