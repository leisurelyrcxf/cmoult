#parsed

from pymoult.highlevel.updates import *
from pymoult.highlevel.managers import *
from pymoult.lowlevel.data_access import DataAccessor
from pymoult.lowlevel.alterability import isFunctionInAnyStack
from pymoult.lowlevel.data_update import updateToClass
import sys

main = sys.modules["__main__"]

#Updating the Page class so it tells the login in use
class PageV2(main.Page):
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
class SessionV2(main.Session):
    session_id = main.Session.session_id
    def __init__(self,items,login,session_id=None):
        self.login = login
        self.values = items
        if session_id and session_id <= SessionV2.session_id:
            self.session_id = session_id
        else:
            self.session_id = SessionV2.session_id
            SessionV2.session_id += 1

        
class User(object):
    def __init__(self,login,passwd):
        self.login = login
        self.passwd = passwd

    def log_in(self,passwd):
        return passwd == self.passwd

#Using eager update to update pages
pageUpd = EagerConversionUpdate(main.pageManager,main.Page,PageV2,None)
pageUpd.setup()
pageUpd.apply()
pageUpd.wait_update()



#Using Lazy update for sessions

def session_trans(obj):
    if not hasattr(obj,"login"):
        obj.login = "anonymous"

sessionUpd = LazyConversionUpdate(main.sessionManager,main.Session,SessionV2,session_trans,None)
sessionUpd.setup()
sessionUpd.apply()


#The login page 
class WebServerV2(main.WebServer):
    def addSession(self,cookie=None):
        cdict = {}
        session_id = None
        login="anonymous"
        for pageK in self.pages.keys():
            cdict[pageK] = 0
        if cookie:
            for key in cookie.keys():
                if key == "session_id":
                    session_id =int(cookie[key].value)
                elif key == "login":
                    login = cookie[key].value
                else:
                    cdict[key] = cookie[key].value
        s = SessionV2(cdict,login,session_id)
        self.sessions[str(s.get_id())] = s
        return s

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


def create_new_do_GET(webserver):
    def new_do_GET(handler):
        path = handler.path.lstrip("/")
        session = handler.getSession()
        if path.startswith("logged"):
            l = path[7:].split("&")
            login = l[0][6:]
            passwd = l[1][9:]
            if login in webserver.users.keys():
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
            handler.wfile.write(page)
        elif path in webserver.pages.keys():
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
            handler.wfile.write(page)
        else:
            handler.send_response(404)
            handler.send_error(404, "Page not found")
    return new_do_GET



class WebManager(ThreadedManager):
    def __init__(self):
        #Get the instance of webserver using immediate access strategy
        da = DataAccessor(main.WebServer,strategy="immediate")
        self.server = None
        for ws in da:
            self.server = ws
        super(WebManager,self).__init__()

    def is_alterable(self):
        return not isFunctionInAnyStack(self.server.Handler.do_GET)

    def update_function(self):
        self.server.pages["login"] = loginPage
        self.server.pages["logged"] = loggedPage
        self.server.pages["nlogged"] = notLogged
        self.server.users = {"bob":User("bob","alice")}
        updateToClass(self.server,WebServerV2)
        self.server.Handler.do_GET = create_new_do_GET(self.server)
    
    def is_over(self):
        return True

webManager = WebManager()
webManager.start()

webUpdate = ThreadedUpdate(webManager)
webUpdate.apply()
webUpdate.wait_update()




