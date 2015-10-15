#parsed

############################################################
#
# Pymoult dynamic patch for pyftpdlib v1.2.0 to v1.3.0
#
############################################################

# New code
###########

#ioloop.py

import errno
import sys

_RETRY = frozenset((errno.EAGAIN, errno.EWOULDBLOCK))


#AsyncChat
def send(self, data):
    try:
        return self.socket.send(data)
    except socket.error:
        why = sys.exc_info()[1]
        if why.args[0] in _RETRY:
            return 0
        elif why.args[0] in _DISCONNECTED:
            self.handle_close()
            return 0
        else:
            raise

def recv(self, buffer_size):
    try:
        data = self.socket.recv(buffer_size)
    except socket.error:
        why = sys.exc_info()[1]
        if why.args[0] in _DISCONNECTED:
            self.handle_close()
            return b('')
        else:
            raise
    else:
        if not data:
            # a closed connection is indicated by signaling
            # a read condition, and having recv() return 0.
            self.handle_close()
            return b('')
        else:
            return data
        

#servers.py

#Class FTPServer
import socket


def __init__(self, address_or_socket, handler, ioloop=None, backlog=5):
    Acceptor.__init__(self, ioloop=ioloop)
    self.handler = handler
    self.backlog = backlog
    self.ip_map = []
    # in case of FTPS class not properly configured we want errors
    # to be raised here rather than later, when client connects
    if hasattr(handler, 'get_ssl_context'):
        handler.get_ssl_context()
    if callable(getattr(address_or_socket, 'listen', None)):
        sock = address_or_socket
        sock.setblocking(0)
        self.set_socket(sock)
        if hasattr(sock, 'family'):
            self._af = sock.family
        else:
            # python 2.4
            ip, port = self.socket.getsockname()[:2]
            self._af = socket.getaddrinfo(ip, port, socket.AF_UNSPEC,
                                          socket.SOCK_STREAM)[0][0]
    else:
        self._af = self.bind_af_unspecified(address_or_socket)
    self.listen(backlog)


#Class _SpawnerBase
from pyftpdlib.ioloop import IOLoop
import select
import os

def _loop(self, handler):
    """Serve handler's IO loop in a separate thread or process."""
    ioloop = IOLoop()
    try:
        handler.ioloop = ioloop
        try:
            handler.add_channel()
        except EnvironmentError:
            err = sys.exc_info()[1]
            if err.errno == errno.EBADF:
                # we might get here in case the other end quickly
                # disconnected (see test_quick_connect())
                return
            else:
                raise

        # Here we localize variable access to minimize overhead.
        poll = ioloop.poll
        sched_poll = ioloop.sched.poll
        poll_timeout = getattr(self, 'poll_timeout', None)
        soonest_timeout = poll_timeout

        while (ioloop.socket_map or ioloop.sched._tasks) and not \
              self._exit.is_set():
            try:
                if ioloop.socket_map:
                    poll(timeout=soonest_timeout)
                if ioloop.sched._tasks:
                    soonest_timeout = sched_poll()
                    # Handle the case where socket_map is emty but some
                    # cancelled scheduled calls are still around causing
                    # this while loop to hog CPU resources.
                    # In theory this should never happen as all the sched
                    # functions are supposed to be cancel()ed on close()
                    # but by using threads we can incur into
                    # synchronization issues such as this one.
                    # https://code.google.com/p/pyftpdlib/issues/detail?id=245
                    if not ioloop.socket_map:
                        ioloop.sched.reheapify() # get rid of cancel()led calls
                        soonest_timeout = sched_poll()
                        if soonest_timeout:
                            time.sleep(min(soonest_timeout, 1))
                else:
                    soonest_timeout = None
            except (KeyboardInterrupt, SystemExit):
                # note: these two exceptions are raised in all sub
                # processes
                self._exit.set()
            except select.error:
                # on Windows we can get WSAENOTSOCK if the client
                # rapidly connect and disconnects
                err = sys.exc_info()[1]
                if os.name == 'nt' and err.args[0] == 10038:
                    for fd in list(ioloop.socket_map.keys()):
                        try:
                            select.select([fd], [], [], 0)
                        except select.error:
                            try:
                                logger.info("discarding broken socket %r",
                                            ioloop.socket_map[fd])
                                del ioloop.socket_map[fd]
                            except KeyError:
                                # dict changed during iteration
                                pass
                else:
                    raise
            else:
                if poll_timeout:
                    if soonest_timeout is None \
                       or soonest_timeout > poll_timeout:
                        soonest_timeout = poll_timeout
    finally:
        ioloop.close()

def handle_accepted(self, sock, addr):
    handler = FTPServer.handle_accepted(self, sock, addr)
    if handler is not None:
        # unregister the handler from the main IOLoop used by the
        # main thread to accept connections
        self.ioloop.unregister(handler._fileno)
        
        t = self._start_task(target=self._loop, args=(handler,))
        t.name = repr(addr)
        t.start()
        
        # it is a different process so free resources here
        if hasattr(t, 'pid'):
            handler.close()
            
        self._lock.acquire()
        try:
            # clean finished tasks
            for task in self._active_tasks[:]:
                if not task.is_alive():
                    self._active_tasks.remove(task)
            # add the new task
            self._active_tasks.append(t)
        finally:
            self._lock.release()


# Updating code
################

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *
from pymoult.highlevel.managers import *

#ioloop.py

ioloop = sys.modules["pyftpdlib.ioloop"]
ioloop._RETRY=_RETRY

asyncchat1up = SafeRedefineMethodUpdate(ioloop.AsyncChat,ioloop.AsyncChat.send,send,"asyncchat1")
asyncchat2up = SafeRedefineMethodUpdate(ioloop.AsyncChat,ioloop.AsyncChat.recv,recv,"asyncchat2")

#servers.py

servers = sys.modules["pyftpdlib.servers"]

ftpserver1up = SafeRedefineMethodUpdate(servers.FTPServer,servers.FTPServer.__init__,__init__,"ftpserver1")

spawner1up = SafeRedefineMethodUpdate(servers._SpawnerBase,servers._SpawnerBase._loop,_loop,"spawner1")
spawner2up = SafeRedefineMethodUpdate(servers._SpawnerBase,servers._SpawnerBase.handle_accepted,handle_accepted,"spawner2")

#Fetch manager from previous update 

manager = fetch_manager("manager")

manager.add_update(asyncchat1up)
manager.add_update(asyncchat2up)
manager.add_update(ftpserver1up)
manager.add_update(spawner1up)
manager.add_update(spawner2up)



