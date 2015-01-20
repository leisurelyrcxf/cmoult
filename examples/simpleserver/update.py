#parsed

import sys
main = sys.modules["__main__"]

    
class SiteV2(object):
    number = main.Site.number
    
    def __init__(self,name,owner):
        self.name = name
        self.number = SiteV2.number
        Site.number+=1
        self.pages = []
        self.owner = owner

    def get_page(self,name):
        return find_name_in_list(name,self.pages)

    def add_page(self,name):
        self.pages.append(Page(name))

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
        Account.number+=1

    def can_access(self,site):
        return site.owner == self

    def add_friend(self,friend):
        self.friends.append(friend)

    def is_friend_with(friend):
        return friend in self.friends

    def __str__(self):
        return "Account of "+self.user+" of id "+str(self.number)

def do_commandV2(comm):
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
    elif comm.startswith("befriend "):
        do_befriend(comm.lstrip("befriend").strip())

def check_access(site):
    if main.current_user != None:
        return main.current_user.can_access(site) or main.current_user.is_friend_with(site.owner)
    return False

def do_befriend(comm):
    if current_user != None:
    ul = filter(lambda x : x.user == comm.strip(),users)
    if len(ul) == 1 and not main.current_user.is_friend_with(ul[0]):
        main.current_user.add_friend(ul[0])

def do_create(comm):
    if current_user != None:
        l = comm.strip().split()
        site = find_name_in_list(l[1],sites)
        if l[0] == "site":
            if not site:
                sites.append(Site(l[1],current_user))
            elif l[0] == "page":
                if site and not site.get_page(l[2]) and check_access(site):
                    site.add_page(l[2])

def do_delete2(comm):
    l = comm.strip().split()
    site = find_name_in_list(l[1],sites)
    if check_access(site):
        if l[0] == "site":
            if site:
                sites.remove(site)
            elif l[0] == "page":
                if site and site.get_page(l[2]):
                    site.delete_page(l[2])

def do_show2(comm):
    l = comm.strip().split()
    if l[0] == "all":
        for s in sites:
            if check_access(s):
                print(s)
    else:
        site = find_name_in_list(l[1],sites)
        if l[0] == "site":
            if site and check_access(site):
                print(site)
        elif l[0] == "page":
            if site and site.get_page(l[2]) and check_access(site):
                print(site.get_page(l[2]))


#K42
#Lazy update for hotswaping 
# Quiescence detected

#Kitsune
#Safe point
#Eager
#Reboot


#DynamOS
