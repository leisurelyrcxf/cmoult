#!/usr/bin/pypy-dsu
"""Simple server that serves pictures from folders""" 

import socket
import sys
import os
import threading
import tempfile

class Picture(object):
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

files = {}

def get_folders():
    for path in sys.argv[1:]:
        if os.path.exists(path):
            files[path] = []
            for pic in os.listdir(path):
                files[path].append(Picture(os.path.join(path,pic),pic))

class ConnThread(threading.Thread):
    def __init__(self,connection):
        self.connection = connection
        self.welcome = "Welcome to the server. Here are the available folders "+" ".join(files.keys())+".\nPlease send the folder you want to download\n"
        self.help = "help : shows this help\nexit : disconnects\ncomment <folder> <comment>: sets commentary for picturesof folder\n<folder name> : downloads pictures from the folder\n(Available folders : "+" ".join(files.keys())+")\n"
        threading.Thread.__init__(self)
        
    def serve_folder(self,folder):
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
        
    def do_command(self,command):
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
                                    
    def run(self):
        self.connection.sendall(self.welcome)
        while self.connection:
            data = self.connection.recv(1024)
            self.do_command(data.strip())
            data = ""
            
def main():
    #Get all folders
    get_folders()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((socket.gethostname(),8080))
    #sock.bind(("10.29.229.31",8080))
    sock.listen(5)
    while True:
        conn,addr = sock.accept()
        ConnThread(conn).start()

if __name__ == "__main__":
    main()
        

    
        












