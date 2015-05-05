#!/usr/bin/pypy-dsu
"""Simple server that serves pictures from folders""" 

import sys
import os
import tempfile

main = sys.modules["__main__"]

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
        self.commentary = text

    def annotate(self):
        new_file = os.path.join(tempfile.gettempdir(),os.path.basename(self.basepath)+"_anot.jpg")
        self.path = new_file
        os.system("convert "+self.basepath+" -background Plum -font Corsiva -pointsize 24 label:'"+self.commentary+"' -gravity Center -append "+self.path)


help = "help : shows this help\nexit : disconnects\ncomment <folder> <comment>: sets commentary for picturesof folder\n<folder name> : downloads pictures from the folder\n(Available folders : "+" ".join(main.files.keys())+")\n"

        
def serve_folder_v2(self,folder):
    self.connection.sendall("serving")
    if self.connection.recv(1024).strip() == "go":
        for pic in files[folder]:
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
    if command in files.keys():
        self.serve_folder(command)
    elif command == "exit":
        self.connection.sendall("terminating")
        self.connection.close()
        self.connection = None
    elif command[0:7] == "comment":
        args = command.split()
        if len(args)> 2:
            if args[1] in files.keys():
                for pic in files[args[1]]:
                    pic.comment(" ".join(args[2:]))
                self.connection.sendall("Comment '"+" ".join(args[2:])+"' applied to folder "+args[1])
    else:
        print(command[0:7])
        self.connection.sendall(self.help)
                                    
            
    
        












