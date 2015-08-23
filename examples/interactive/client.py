#!/usr/bin/python

import socket
import sys
import re
import math


if len(sys.argv) < 2:
    print("usage : client.py host")
    sys.exit(1)

host = sys.argv[1]
imgpattern = re.compile("\<img\:([0-9]+)\>(.*)")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect((host,8080))

def recv():
    res_strip = b''
    while len(res_strip) == 0:
        res = sock.recv(1024)
        res_strip = res.strip()
    if res_strip.isdigit():
        length = int(res_strip)
        ans = b''
        while (length > 0):
            res = sock.recv(min(1024,length))
            length -= len(res)
            ans+=res
        res_strip = ans.strip()
    return res_strip
    

def send(string):
    sock.sendall(string.ljust(1024))


try:
    welcome = recv()
    print(welcome.decode("utf-8"))
    while True:
        command = input("$ ")
        if command.strip() != "": 
            sock.send(str.encode(command.strip()))
            response = recv()
            if response == b"serving":
                print("downloading folder")
                sock.send(b"go")
                while True:
                    response = recv()
                    catch = imgpattern.match(response.decode("utf-8"))
                    if catch is not None:
                        length = int(catch.group(1))
                        pic = catch.group(2)
                        print("downloading "+pic)
                        send(b"ok")
                        stream = recv()
                        f = open(pic,"wb")
                        f.write(stream)
                        f.close()
                        sock.sendall(b"ok")
                    elif response == b"finished":
                        print("downlad finished")
                        break
                    else:
                        send(b"cancel")
            elif response == b"terminating":
                sock.close()
                break
            else:
                print(response.decode("utf-8"))
                
except KeyboardInterrupt:
    send(b"exit")
    sock.close()















