#!/usr/bin/python-dsu3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

#import Pymoult
from pymoult.highlevel.listener import Listener
from pymoult.threads import DSU_Thread

#Initialize a simple ftp server
authorizer = DummyAuthorizer()
authorizer.add_anonymous(os.path.abspath("data"))

handler = FTPHandler
handler.authorizer = authorizer
handler.banner = "Bruce"

address = ('127.0.0.1',2121)
server = FTPServer(address,handler)

server.max_cons = 256
server.max_cons_per_ip = 5


#Start Pymoult Listener
listener = Listener()
listener.start()

def main():
    server.serve_forever(timeout=0.5)

mainThread = DSU_Thread(target=main,name="mainThread")
mainThread.start()
