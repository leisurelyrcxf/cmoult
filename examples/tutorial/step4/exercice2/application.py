from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from threading import Thread

class Page(object):
    def __init__(self,path,title,content):
        self.path = path
        self.title = title
        self.content = content
    
    def call(self,session):
        self.n = int(session.values[self.path]) + 1
        session.values[self.path] = str(self.n)

    def __str__(self):
       s = "<html><head><title>"+self.title+"</title></head>"
       s+= "<body><h1>"+self.title+"</h1>"
       s+= "<p>"+self.content+"</p>"
       s+= "<p>You saw this page "+str(self.n)+" times</p></body></html>"
       return s

class Session(object):
    session_id = 0
    def __init__(self,items,session_id=None):
        self.values = items
        if session_id and session_id <= Session.session_id:
            self.session_id = session_id
        else:
            self.session_id = Session.session_id
            Session.session_id += 1

    def get_id(self):
        return self.session_id

    def cookie(self):
        c = SimpleCookie()
        for key in list(self.values.keys()):
            c[key] = self.values[key]
        c["session_id"] = self.session_id
        return c

#The Handler class needs to be generated for a specific webserver.
#We therefore define a function that generates a Handler class for a given webserver 
def produceHandler(webserver):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = self.path.lstrip("/")
            if path in list(webserver.pages.keys()):
                session = self.getSession()
                page = webserver.pages[path]
                page.call(session)
                #Response OK
                self.send_response(200)
                #Headers including the cookie
                self.send_header("Content-type","text/html")
                self.send_header("Set-Cookie", session.cookie().output(header=""))
                self.end_headers()
                self.wfile.write(str(page).encode("ascii"))
            else:
                self.send_response(404)
                self.send_error(404, "Page not found")

        def getSession(self):
            #If the navigator already has a session opened
            if "Cookie" in self.headers:
                c = SimpleCookie(self.headers["Cookie"])
                #If thenavigator's session matches a session object 
                if c["session_id"].value in list(webserver.sessions.keys()):
                    return webserver.sessions[c["session_id"].value]
                #Else, we create a new session object
                else:
                    return webserver.addSession(c)
            #If the navigator does not have a session opened
            else:
                #We create a new session object
                return webserver.addSession()

    return Handler


class WebServer(object):
    def __init__(self,pages):
        self.pages = {}
        for page in pages:
            self.pages[page.path] = page
        #Generate a Handler class specifically for the current Webserver.
        self.Handler = produceHandler(self)
        self.sessions = {}

    def addSession(self,cookie=None):
        cdict = {}
        session_id = None
        for pageK in list(self.pages.keys()):
            cdict[pageK] = 0
        if cookie:
            for key in list(cookie.keys()):
                if key == "session_id":
                    session_id =int(cookie[key].value)
                else:
                    cdict[key] = cookie[key].value
        s = Session(cdict,session_id)
        self.sessions[str(s.get_id())] = s
        return s
    
    def run(self):
        #Create a http server listening on localhost port 8080
        #The server will use the self.Handler class to handle the clients requests
        httpd = HTTPServer(("",8080),self.Handler)
        while True:
            staticUpdatePoint()
            httpd.handle_request()

def main():
    p1 = Page("banana","Banana!","A nice fruit. Allways bring one to parties")
    p2 = Page("coconut","Coconut","A fine coconut")
    p3 = Page("hello","Hello World!","Hello!")
    pages = [p1,p2,p3]
    ws = WebServer(pages)
    ws.run()

#Setup the main thread
main_thread = Thread(target=main)
main_thread.start()
