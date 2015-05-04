#!/usr/bin/pypy-dsu
"""Simple server that serves pictures from folders""" 

import socket
import sys
import os
import threading


class Picture(object):
    def __init__(self,path):
        self.path = path

    def stream(self):
        f = open(self.path,'r')
        stream = f.read()
        f.close()
        return stream

all_folders = []

def get_folders():
    for path in sys.argv[1:]:
        if os.path.exists(path):
            all_folders.append(path)

class ConnThread(threading.Thread):
    def __init__(self,connection):
        self.connection = connection
        self.welcome = "Welcome to the server. Here are the available folders "+" ".join(all_folders)+".\nPlease send the folder you want to download\n"
        self.help = "help : shows this help\nexit : disconnects\n<folder name> : downloads pictures from the folder\n(Available folders : "+" ".join(all_folders)+")\n"
        threading.Thread.__init__(self)
        
    def serve_folder(self,folder):
        self.connection.sendall("serving")
        if self.connection.recv(1024).strip() == "go":
            for pic in os.listdir(folder):
                imgstream = Picture(os.path.join(folder,pic)).stream()
                self.connection.sendall("<img:"+str(len(imgstream))+">"+pic)
                if self.connection.recv(1024).strip() == "cancel":
                    return
                self.connection.sendall(imgstream)
                if self.connection.recv(1024).strip() == "cancel":
                    return
            self.connection.sendall("finished")
        
    def do_command(self,command):
        if command in all_folders:
            self.serve_folder(command)
        elif command == "exit":
            self.connection.sendall("terminating")
            self.connection.close()
            self.connection = None
        else:
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
        

    
        












