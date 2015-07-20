#parsed



from pymoult.highlevel.managers import ThreadedManager
from pymoult.highlevel.updates import LazyConversionUpdate,SafeRedefineUpdate,Update
from pymoult.lowlevel.data_update import redefineClass
import sys
main = sys.modules["__main__"]

    
class SiteV2(object):
    number = main.Site.number
    
    def __init__(self,name,owner):
        self.name = name
        self.number = main.Site.number
        main.Site.number+=1
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
        self.number = main.Account.number
        main.Account.number+=1

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
        main.do_create(comm.lstrip("create").strip())
    elif comm.startswith("delete "):
        main.do_delete(comm.lstrip("delete").strip())
    elif comm.startswith("show "):
        main.do_show(comm.lstrip("show").strip())
    elif comm.startswith("login "):
        main.do_login(comm.lstrip("login").strip())
    elif comm.startswith("logout"):
        main.do_logout(comm.lstrip("logout").strip())
    elif comm.startswith("register "):
        main.do_register(comm.lstrip("register").strip())
    elif comm.startswith("befriend "):
        do_befriend(comm.lstrip("befriend").strip())

def check_access(site):
    if main.current_user != None:
        return main.current_user.can_access(site) or main.current_user.is_friend_with(site.owner) or site.owner == None
    return False

def do_befriend(comm):
    if main.current_user != None:
        ul = list(filter(lambda x : x.user == comm.strip(),main.users))
    if len(ul) == 1 and not main.current_user.is_friend_with(ul[0]):
        main.current_user.add_friend(ul[0])

def do_createV2(comm):
    if main.current_user != None:
        l = comm.strip().split()
        site = main.find_name_in_list(l[1],main.sites)
        if l[0] == "site":
            if not site:
                main.sites.append(main.Site(l[1],main.current_user))
        elif l[0] == "page":
            if site and not site.get_page(l[2]) and check_access(site):
                site.add_page(l[2])

def do_deleteV2(comm):
    l = comm.strip().split()
    site = main.find_name_in_list(l[1],main.sites)
    if check_access(site):
        if l[0] == "site":
            if site:
                sites.remove(site)
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


#Start the managers
account_manager = ThreadedManager(threads=[main.main_thread])
account_manager.start()
site_manager = ThreadedManager(threads=[main.main_thread])
site_manager.start()
functions_manager = ThreadedManager(threads=[main.main_thread])
functions_manager.start()


def transformer_site(site):
    site.owner = None

def transformer_account(account):
    account.friends=[]

site_update = LazyConversionUpdate(main.Site,SiteV2,transformer_site,None)
account_update = LazyConversionUpdate(main.Account,AccountV2,transformer_account,None)
account_manager.add_update(account_update)
site_manager.add_update(site_update)

class ClassUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        redefineClass(main,main.Site,SiteV2)
        redefineClass(main,main.Account,AccountV2)

clsupdate = ClassUpdate()
functions_manager.add_update(clsupdate)
    
do_command_update = SafeRedefineUpdate(main,main.do_command,do_commandV2)
functions_manager.add_update(do_command_update)
do_create_update = SafeRedefineUpdate(main,main.do_create,do_createV2)
functions_manager.add_update(do_create_update)
do_delete_update = SafeRedefineUpdate(main,main.do_delete,do_deleteV2)
functions_manager.add_update(do_delete_update)
do_show_update = SafeRedefineUpdate(main,main.do_show,do_showV2)
functions_manager.add_update(do_show_update)

class EmptyUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        pass
    def cleanup(self):
        print("Update finished")

functions_manager.add_update(EmptyUpdate())
