#parsed
from pymoult.highlevel.updates import EagerConversionUpdate,LazyConversionUpdate
from pymoult.highlevel.managers import LazyConversionManager
from pymoult.lowlevel.data_access import DataAccessor
from pymoult.lowlevel.alterability import wait_static_points
from pymoult.lowlevel.data_update import updateToClass,addFieldToClass
from pymoult.lowlevel.stack import resumeThread
import sys


main = sys.modules["__main__"]

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

#Fortunately, we started a EagerConversionManager that did the work
#for the step 1 ;)

da = DataAccessor(main.WebServer,strategy="immediate")
server = None
for ws in da:
    server = ws

#Then, we add the static pages to the webserver
server.pages['login'] = loginPage
server.pages['logged'] = loggedPage
server.pages['nlogged'] = notLogged
    
#We add a users attribute to the server, containing the users
#We add a new user "bob" with password "alice"
server.users = {"bob":User("bob","alice")}


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


# First, we need to consider the alterability of the application.  We
# will place a staticUpdatePoint in the "run" method of the webserver,
# at the begining of the while loop.

#We will wait for the main_thread to reach that update point

wait_static_points([main.main_thread])
#The static point has been reached !!!
#Let's continue the update

#To update the addSession method of the webserver, we need to update the WebServer class
updateToClass(server,WebServerV2)

#We need to change the do_GET method of the Handler class possesed by the server
handler = server.Handler
#We create a new do_GET method using create_new_do_GET and set it to the handler class
addFieldToClass(handler,"do_GET",create_new_do_GET(server))


#We have finished the update, we need to resume the execution of the Thread
resumeThread(main.main_thread)


print("UPDATE COMPLETE")


