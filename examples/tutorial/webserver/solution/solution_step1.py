#parsed
from pymoult.highlevel.updates import EagerConversionUpdate,LazyConversionUpdate,Update
from pymoult.lowlevel.data_access import DataAccessor
from pymoult.lowlevel.alterability import waitStaticPoints
from pymoult.lowlevel.data_update import updateToClass,addFieldToClass
from pymoult.lowlevel.stack import resumeThread
import sys

from Cookie import SimpleCookie


main = sys.modules["__main__"]

#Step one : Updating the pages and the sessions

#Updating the Page class so it tells the login in use
class PageV2(object):
    def __init__(self,path,title,content):
        self.path = path
        self.title = title
        self.content = content
  
    def call(self,session):
        self.n = int(session.values[self.path]) + 1
        session.values[self.path] = str(self.n)
        self.name = session.login

    def __str__(self):
       s = "<html><head><title>"+self.title+"</title></head>"
       s+= "<body><h1>"+self.title+"</h1>"
       s+= "<p>"+self.content+"</p>"
       s+= "<p>"+self.name+", you saw this page "+str(self.n)+" times</p></body></html>"
       return s

#Class Session with login support
class SessionV2(object):
    session_id = main.Session.session_id
    def __init__(self,items,login,session_id=None):
        self.login = login
        self.values = items
        if session_id and session_id <= SessionV2.session_id:
            self.session_id = session_id
        else:
            self.session_id = SessionV2.session_id
            SessionV2.session_id += 1

    def get_id(self):
        return self.session_id

    def cookie(self):
        c = SimpleCookie()
        for key in self.values.keys():
            c[key] = self.values[key]
        c["session_id"] = self.session_id
        return c

#Using Lazy conversion for sessions

#Create a transformer
#Each session opened before the update will be considered as "anonymous" session
def session_trans(obj):
    obj.login = "anonymous"

#Start the conversion with the Update class
sessionUpd = LazyConversionUpdate(main.Session,SessionV2,session_trans)
main.manager.add_update(sessionUpd)

#Using eager update to update pages

#We need to enable the eager manager when starting the application !!!

pageUpd = EagerConversionUpdate(main.Page,PageV2,None)
main.manager.add_update(pageUpd)

