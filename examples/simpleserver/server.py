#!/usr/bin/python-dsu3


import socket
from pymoult.highlevel.listener import Listener
from pymoult.threads import DSU_Thread

hostname = "localhost"
port = 8080
max_connections = 10
max_data_length = 999


sites = []

users = []

current_user = None

def find_name_in_list(name,l):
    ll = filter(lambda x : x.name == name,l)
    if len(ll) > 0:
        return ll[0]
    else:
        return None

class Site(object):
    number = 0
    def __init__(self,name):
        self.name = name
        self.number = Site.number
        Site.number+=1
        self.pages = []

    def get_page(self,name):
        return find_name_in_list(name,self.pages)

    def add_page(self,name):
        self.pages.append(Page(name))

    def delete_page(self,name):
        self.pages.remove(self.get_page(name))

    def __str__(self):
        return "A site named "+self.name+" of id "+str(self.number)+"\n pages :\n"+"\n".join(map(str,self.pages)) 
        

class Page(object):
    number = 0
    def __init__(self,name):
        self.name = name
        self.number = Page.number
        Page.number+=1

    def __str__(self):
        return "A Page named "+self.name+" of id "+str(self.number)

class Account(object):
    number = 0
    def __init__(self,user):
        self.user = user
        self.number = Account.number
        Account.number+=1

    def __str__(self):
        return "Account of "+self.user+" of id "+str(self.number)


def do_create(comm):
    l = comm.strip().split()
    site = find_name_in_list(l[1],sites)
    if l[0] == "site":
        if not site:
            sites.append(Site(l[1]))
    elif l[0] == "page":
        if site and not site.get_page(l[2]):
            site.add_page(l[2])

def do_delete(comm):
    l = comm.strip().split()
    site = find_name_in_list(l[1],sites)
    if l[0] == "site":
        if site:
            sites.remove(site)
    elif l[0] == "page":
        if site and site.get_page(l[2]):
            site.delete_page(l[2])
    
def do_show(comm):
    l = comm.strip().split()
    if l[0] == "all":
        for s in sites:
            print(s)
    else:
        site = find_name_in_list(l[1],sites)
        if l[0] == "site":
            if site:
                print(site)
        elif l[0] == "page":
            if site and site.get_page(l[2]):
                print(site.get_page(l[2]))

def do_login(comm):
    global current_user
    ul = filter(lambda x : x.user == comm.strip(),users)
    if len(ul) == 1:
        current_user = ul[0]
        print("User "+comm.strip()+" logged in")
 

def do_logout(comm):
    global current_user
    if current_user != None:
        current_user = None
    
def do_register(comm):
    ul = filter(lambda x : x.user == comm.strip(),users)
    if len(ul) == 0:
        users.append(Account(comm.strip()))
    

def do_command(comm):
    if comm.startswith("create "):
        do_create(comm.lstrip("create").strip())
    elif comm.startswith("delete "):
        do_delete(comm.lstrip("delete").strip())
    elif comm.startswith("show "):
        do_show(comm.lstrip("show").strip())
    elif comm.startswith("login "):
        do_login(comm.lstrip("login").strip())
    elif comm.startswith("logout "):
        do_logout(comm.lstrip("logout").strip())
    elif comm.startswith("register "):
        do_register(comm.lstrip("register").strip())

def main_loop():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((hostname,port))
    s.listen(max_connections)
    while True:
        conn,addr = s.accept()
        data = conn.recv(max_data_length)
        do_command(data.decode("ascii"))
        data = ""
        conn.close()

if __name__ == "__main__":
    listener = Listener()
    listener.start()
    main_thread = DSU_Thread(name="main thread",target=main_loop)
    print("Starting server")
    main_thread.start()

