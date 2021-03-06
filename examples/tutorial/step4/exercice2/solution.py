#parsed
from pymoult.highlevel.updates import EagerConversionUpdate,LazyConversionUpdate,Update,isApplied
from pymoult.lowlevel.data_access import DataAccessor
from pymoult.lowlevel.alterability import waitStaticPoints,setupWaitStaticPoints,cleanFailedStaticPoints
from pymoult.lowlevel.data_update import updateToClass,addFieldToClass
import sys

from http.cookies import SimpleCookie


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
        for key in list(self.values.keys()):
            c[key] = self.values[key]
        c["session_id"] = self.session_id
        return c

#Using Lazy conversion for sessions

#Create a transformer
#Each session opened before the update will be considered as "anonymous" session
def session_trans(obj):
    obj.login = "anonymous"

#Start the conversion with the Update class
sessionUpd = LazyConversionUpdate(main.Session,SessionV2,session_trans,name="Session")
main.manager.add_update(sessionUpd)

#Using eager update to update pages

#We need to enable the eager manager when starting the application !!!

pageUpd = EagerConversionUpdate(main.Page,PageV2,None,name="Page")
main.manager.add_update(pageUpd)


#Step two : updating the webserver
#We will proceed in 2 substeps : (1) modify its state and (2) modify its methods

#Substep 1 : modifying the state of the webserver

class User(object):
    def __init__(self,login,passwd):
        self.login = login
        self.passwd = passwd

    def log_in(self,passwd):
        return passwd == self.passwd

class StaticPage(main.Page):
    def __init__(self,path,title,content):
        self.path = path
        self.title = title
        self.content = content

    def call(self,session):
        pass

    def __str__(self):
        s = "<html><head><title>"+self.title+"</title></head>"
        s+= "<body><h1>"+self.title+"</h1>"
        s+= "<p>"+self.content+"</p>"
        return s

loginPage = StaticPage("login","You are not logged in!","""
<form method="get" action="logged">
Login : <input type="text" name="login">
Password: <input type="password" name="password">
<input type="submit" value="Log in">
</form>
""")

loggedPage = StaticPage("logged","Logged in!","You are logged in!")
notLogged = StaticPage("nlogged","Login failed","You are not logged in")


#First we need to retrieve the webserver, for this purpose we will use
#the DataAccessor from the lowlevel API

#Remember : using the immediate strategy requires the ObjectPool to be
#created before creating the webserver !!

class WebServerStateUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        da = DataAccessor(main.WebServer,strategy="immediate")
        #Because we'll need it for the next update,
        #we store the server in the manager
        self.manager.server = None
        for ws in da:
            self.manager.server = ws
        #Then, we add the static pages to the webserver
        self.manager.server.pages['login'] = loginPage
        self.manager.server.pages['logged'] = loggedPage
        self.manager.server.pages['nlogged'] = notLogged
        #We add a users attribute to the server, containing the users
        #We add a new user "bob" with password "alice"
        self.manager.server.users = {"bob":User("bob","alice")}

serverUpdate1 = WebServerStateUpdate(name="WebServerState")
main.manager.add_update(serverUpdate1)

#Substep 2 :  modifiy the methods of the webserver

class WebServerV2(object):
    def __init__(self,pages):
        self.pages = {}
        for page in pages:
            self.pages[page.path] = page
        #Generate a Handler class specifically for the current Webserver.
        self.Handler = produceHandler(self)
        self.sessions = {}
        self.users = {}

    def addSession(self,cookie=None):
        cdict = {}
        session_id = None
        login="anonymous"
        for pageK in list(self.pages.keys()):
            cdict[pageK] = 0
        if cookie:
            for key in list(cookie.keys()):
                if key == "session_id":
                    session_id =int(cookie[key].value)
                elif key == "login":
                    login = cookie[key].value
                else:
                    cdict[key] = cookie[key].value
        s = SessionV2(cdict,login,session_id)
        self.sessions[str(s.get_id())] = s
        return s

    def run(self):
        #Create a http server listening on localhost port 8080
        #The server will use the self.Handler class to handle the clients requests
        httpd = HTTPServer(("",8080),self.Handler)
        while True:
            staticUpdatePoint()
            httpd.handle_request()
    

def create_new_do_GET(webserver):
    def new_do_GET(handler):
        path = handler.path.lstrip("/")
        session = handler.getSession()
        if path.startswith("logged"):
            l = path[7:].split("&")
            login = l[0][6:]
            passwd = l[1][9:]
            if login in list(webserver.users.keys()):
                user = webserver.users[login]
                if user.log_in(passwd):
                    path="logged"
                    session.login = login
                else:
                    path="nlogged"
            else:
                path = "nlogged"
            page = webserver.pages[path]
            handler.send_response(200)
            handler.send_header("Content-type","text/html")
            handler.end_headers()
            handler.wfile.write(str(page).encode("ascii"))
        elif path in list(webserver.pages.keys()):
            if session.login == "anonymous":
                page = webserver.pages["login"]
            else:
                page = webserver.pages[path]
            page.call(session)
            #Response OK
            handler.send_response(200)
            #Headers including the cookie
            handler.send_header("Content-type","text/html")
            handler.send_header("Set-Cookie", session.cookie().output(header=""))
            handler.end_headers()
            handler.wfile.write(str(page).encode("ascii"))
        else:
            handler.send_response(404)
            handler.send_error(404, "Page not found")
    return new_do_GET


# First, we need to consider the alterability of the application.  We
# will place a staticUpdatePoint in the "run" method of the webserver,
# at the begining of the while loop.

#We will wait for the main_thread to reach that update point

class WebServerUpdate(Update):
    def check_requirements(self):
        #We want to have WebServerState update done
        if isApplied("WebServerState"):
            return "yes"
        else:
            return "no"
    
    def preupdate_setup(self):
        setupWaitStaticPoints([main.main_thread])
    
    def wait_alterability(self):
        return waitStaticPoints([main.main_thread])

    def apply(self):
        #To update the addSession method of the webserver, we need to update the WebServer class
        updateToClass(self.manager.server,main.WebServer,WebServerV2)
        #We need to change the do_GET method of the Handler class possesed by the server
        handler = self.manager.server.Handler
        #We create a new do_GET method using create_new_do_GET and set it to the handler class
        addFieldToClass(handler,"do_GET",create_new_do_GET(self.manager.server))

    def clean_failed_alterability(self):
        cleanFailedStaticPoints([main.main_thread])

    def cleanup(self):
        print("UPDATE COMPLETE")
        return True


webUpdate = WebServerUpdate(name="WebServer")
main.manager.add_update(webUpdate)

