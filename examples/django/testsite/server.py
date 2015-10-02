#!/usr/bin/python-dsu3

import cherrypy
from pymoult.highlevel.listener import PipeListener
from testsite.wsgi import application


if __name__ == '__main__':
    listener = PipeListener()
    listener.start()

    #Start cherrypy 
#    cherrypy.tree.graft(application,"/")
    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 8080
    server.thread_pool = 30
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
