#parsed


from pymoult.highlevel.updates import ThreadRebootUpdate,HeapTraversalUpdate,Update
from pymoult.lowlevel.data_access import HeapWalker
from pymoult.lowlevel.data_update import updateToClass
from pymoult.lowlevel.alterability import get_current_frames,waitStaticPoints,staticUpdatePoint,setupWaitStaticPoints,cleanFailedStaticPoints
from pymoult.lowlevel.stack import resumeThread
import sys
import socket
main = sys.modules["__main__"]

    
class SiteV2(object):
    number = main.Site.number
    
    def __init__(self,name,owner):
        self.name = name
        self.number = SiteV2.number
        SiteV2.number+=1
        self.pages = []
        self.owner = owner

    def get_page(self,name):
        return main.find_name_in_list(name,self.pages)

    def add_page(self,name):
        self.pages.append(main.Page(name))

    def delete_page(self,name):
        self.pages.remove(self.get_page(name))

    def __str__(self):
        return "A site named "+self.name+" of id "+str(self.number)+"\n pages :\n"+"\n".join(map(str,self.pages)) 

class AccountV2(object):
    number = main.Account.number
    def __init__(self,user):
        self.user = user
        self.friends = []
        self.number = AccountV2.number
        AccountV2.number+=1

    def can_access(self,site):
        return site.owner == self

    def add_friend(self,friend):
        self.friends.append(friend)

    def is_friend_with(self,friend):
        return friend in self.friends

    def __str__(self):
        return "Account of "+self.user+" of id "+str(self.number)

def do_commandV2(comm):
    if comm.startswith("create "):
        do_createV2(comm.lstrip("create").strip())
    elif comm.startswith("delete "):
        do_deleteV2(comm.lstrip("delete").strip())
    elif comm.startswith("show "):
        do_showV2(comm.lstrip("show").strip())
    elif comm.startswith("login "):
        main.do_login(comm.lstrip("login").strip())
    elif comm.startswith("logout"):
        main.do_logout(comm.lstrip("logout").strip())
    elif comm.startswith("register "):
        do_registerV2(comm.lstrip("register").strip())
    elif comm.startswith("befriend "):
        do_befriend(comm.lstrip("befriend").strip())

def check_access(site):
    if main.current_user != None:
        return main.current_user.can_access(site) or main.current_user.is_friend_with(site.owner) or site.owner == None
    return False

def do_befriend(comm):
    if main.current_user != None:
        ul = filter(lambda x : x.user == comm.strip(),users)
    if len(ul) == 1 and not main.current_user.is_friend_with(ul[0]):
        main.current_user.add_friend(ul[0])

def do_createV2(comm):
    if main.current_user != None:
        l = comm.strip().split()
        site = main.find_name_in_list(l[1],main.sites)
        if l[0] == "site":
            if not site:
                main.sites.append(SiteV2(l[1],main.current_user))
        elif l[0] == "page":
            if site and not site.get_page(l[2]) and check_access(site):
                site.add_page(l[2])

def do_deleteV2(comm):
    l = comm.strip().split()
    site = main.find_name_in_list(l[1],main.sites)
    if check_access(site):
        if l[0] == "site":
            if site:
                main.sites.remove(site)
            elif l[0] == "page":
                if site and site.get_page(l[2]):
                    site.delete_page(l[2])

def do_showV2(comm):
    l = comm.strip().split()
    if l[0] == "all":
        for s in main.sites:
            if check_access(s):
                print(s)
    else:
        site = main.find_name_in_list(l[1],main.sites)
        if l[0] == "site":
            if site and check_access(site):
                print(site)
        elif l[0] == "page":
            if site and site.get_page(l[2]) and check_access(site):
                print(site.get_page(l[2]))

def do_registerV2(comm):
    ul = filter(lambda x : x.user == comm.strip(),main.users)
    if len(ul) == 0:
        main.users.append(AccountV2(comm.strip()))


def new_main(s):
    while True:
        #This is a safe point for updating
        staticUpdatePoint()
        conn,addr = s.accept()
        data = conn.recv(main.max_data_length)
        do_commandV2(data.decode("ascii"))
        data = ""
        conn.close()

def transform_site(site):
    site.owner = None

def transform_account(account):
    account.friends=[]

class MyHeapWalker(HeapWalker):
    def walk_list(self,lst):
        for item in lst:
            self.walk(item)
    def walk_Account(self,account):
        updateToClass(account,AccountV2,transform_account)
    def walk_Site(self,site):
        updateToClass(site,SiteV2,transform_site)
    def walk_module(self,mod):
        if mod.__name__ == "__main__":
            for item in dir(mod):
                self.walk(mod[item])
            
def get_socket_fromstack():
    frame = get_current_frames()[main.main_thread.ident]
    while frame:
        if frame.f_code is main.main_loop.func_code:
            return frame.f_locals["s"]
        frame = frame.f_back

sock = get_socket_fromstack()

heap_update = HeapTraversalUpdate(MyHeapWalker())
thread_update = ThreadRebootUpdate(main.main_thread,new_main,[sock])

class KitsuneUpdate(Update):
    def preupdate_setup(self):
        setupWaitStaticPoints([main.main_thread])
    
    def wait_alterability(self):
        return waitStaticPoints([main.main_thread])

    def apply(self):
        heap_update.apply()
        print("Heap traveresed and updated")
        thread_update.apply()
        print("Main thread rebooted")

    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.main_thread])

    def cleanup(self):
        print("Update Complete!")

update = KitsuneUpdate()
main.manager.add_update(update)
