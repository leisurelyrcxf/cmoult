#!/usr/bin/python-dsu3
"""Simple server that serves pictures from folders""" 

import socket
import sys
import os
import threading
from pymoult.highlevel.listener import Listener

class Picture(object):
    def __init__(self,path,name):
        self.path = path
        self.name = name

    def stream(self):
        f = open(self.path,'rb')
        stream = f.read()
        f.close()
        return stream


files = {}
helptext = ""

def get_folders():
    for path in sys.argv[1:]:
        if os.path.exists(path):
            files[path] = []
            for pic in os.listdir(path):
                files[path].append(Picture(os.path.join(path,pic),pic))

class ConnThread(threading.Thread):
    def __init__(self,connection):
        self.connection = connection
        self.welcome = "Welcome to the server. Here are the available folders "+" ".join(list(files.keys()))+".\nPlease send the folder you want to download\n"

        threading.Thread.__init__(self)

    def send(self,string):
        l = len(string)
        if l <= 1024:
            res = self.connection.sendall(string.ljust(1024))
        else:
            self.connection.sendall(str.encode(str(l)).ljust(1024))
            length = int(l/1024)*1024+1024
            self.connection.sendall(string.ljust(length))
            
    def recv(self):
        res = self.connection.recv(1024)
        return res.strip()
        
    def serve_folder(self,folder):
        try:
            self.send(b"serving")
            if self.recv() == b"go":
                for pic in files[folder]:
                    imgstream = pic.stream()
                    s = "<img:"+str(len(imgstream))+">"+pic.name
                    self.send(str.encode(s))
                    if self.recv() == b"cancel":
                        return
                    self.send(imgstream)
                    if self.recv() == b"cancel":
                        return
                self.send(b"finished")
        except socket.timeout:
            #Send finish in the client is waiting for it
            self.send(b"finished")
            
    def do_command(self,command):
        if command in list(files.keys()):
            self.serve_folder(command)
        elif command == "exit":
            self.send(b"terminating")
            self.connection.close()
            self.connection = None
        else:
            self.send(str.encode(helptext))
                                    
    def run(self):
        self.connection.sendall(str.encode(self.welcome))
        while self.connection:
            try:
                data = ""
                data = self.recv()
                self.do_command(data.decode("utf-8"))
            except socket.timeout:
                pass
            
def main():
    global helptext
    #Get all folders
    get_folders()
    helptext = "help : shows this help\nexit : disconnects\n<folder name> : downloads pictures from the folder\n(Available folders : "+" ".join(list(files.keys()))+")\n"
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    sock.bind((socket.gethostname(),8080))
    sock.bind(('localhost',8080))
    sock.settimeout(10)
    sock.listen(5)
    while True:
        try:
            conn,addr = sock.accept()
            ConnThread(conn).start()
        except socket.timeout:
            pass

            
if __name__ == "__main__":
    listener = Listener()
    listener.start()
    main()
        

    
        












