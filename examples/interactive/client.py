#!/usr/bin/python2

import socket
import sys
import re


if len(sys.argv) < 2:
    print("usage : client.py host")
    sys.exit(1)

host = sys.argv[1]
imgpattern = re.compile("\<img\:([0-9]+)\>(.*)")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect((host,8080))
try:
    welcome = sock.recv(8192)
    print(welcome.strip())
    while True:
        command = raw_input("$ ")
        sock.sendall(command.strip())
        response = sock.recv(8192)
        if response.strip() == "serving":
            print("downloading folder")
            sock.sendall("go")
            while True:
                response = sock.recv(1024)
                catch = imgpattern.match(response.strip())
                if catch is not None:
                    length = int(catch.group(1))
                    pic = catch.group(2)
                    print("downloading "+pic)
                    sock.sendall("ok")
                    stream = sock.recv(length)
                    f = open(pic,"w")
                    f.write(stream)
                    f.close()
                    sock.sendall("ok")
                elif response.strip() == "finished":
                    print("downlad finished")
                    break
                else:
                    sock.sendall("cancel")
        elif response.strip() == "terminating":
            sock.close()
            break
        else:
            print(response.strip())

except KeyboardInterrupt:
    sock.sendall("exit")
    sock.close()















