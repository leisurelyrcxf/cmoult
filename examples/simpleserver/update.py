#parsed

import sys
main = sys.modules["__main__"]


def do_move(comm):
    l = comm.strip().split()
    siteA = find_name_in_list(l[1],sites)
    siteB = find_name_in_list(l[2],sites)
    if siteA and siteB:
        page = siteA.get_page(l[0])
        if page:
            siteA.sites.append(page)
            siteB.sites.remove(page)

    
class SiteV2(object):
    number = main.Site.number
    
    def __init__(self,name,owner):
        self.name = name
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
        Account.number+=1

    def can_access(self,site):
        return site.owner == self

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
    elif comm.startswith("move "):
        do_move(comm.lstrip("move").strip())


