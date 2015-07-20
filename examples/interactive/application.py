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
        f = open(self.path,'r')
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
        
    def serve_folder(self,folder):
        try:
            self.connection.sendall("serving".encode("ascii"))
            if self.connection.recv(1024).strip() == "go":
                for pic in files[folder]:
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
            
    def do_command(self,command):
        if command in list(files.keys()):
            self.serve_folder(command)
        elif command == "exit":
            self.connection.sendall("terminating".encode("ascii"))
            self.connection.close()
            self.connection = None
        else:
            self.connection.sendall(helptext.encode("ascii"))
                                    
    def run(self):
        self.connection.sendall(self.welcome.encode("ascii"))
        while self.connection:
            try:
                data = ""
                data = self.connection.recv(1024)
                self.do_command(data.decode("utf-8").strip())
            except socket.timeout:
                pass
            
def main():
    global helptext
    #Get all folders
    get_folders()
    helptext = "help : shows this help\nexit : disconnects\n<folder name> : downloads pictures from the folder\n(Available folders : "+" ".join(list(files.keys()))+")\n"
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((socket.gethostname(),8080))
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
        

    
        












