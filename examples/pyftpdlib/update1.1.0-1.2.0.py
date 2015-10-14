#parsed

############################################################
#
# Pymoult dynamic patch for pyftpdlib v1.1.0 to v1.2.0
#
############################################################

# New code
###########

#handlers.py

from pyftpdlib.ioloop import Acceptor
from pyftpdlib.log import logger

class PassiveDTP(Acceptor):
    """Creates a socket listening on a local port, dispatching the
    resultant connection to DTPHandler. Used for handling PASV command.

     - (int) timeout: the timeout for a remote client to establish
       connection with the listening socket. Defaults to 30 seconds.

     - (int) backlog: the maximum number of queued connections passed
       to listen(). If a connection request arrives when the queue is
       full the client may raise ECONNRESET. Defaults to 5.
    """
    timeout = 30
    backlog = None

    def __init__(self, cmd_channel, extmode=False):
        """Initialize the passive data server.

         - (instance) cmd_channel: the command channel class instance.
         - (bool) extmode: wheter use extended passive mode response type.
        """
        self.cmd_channel = cmd_channel
        self.log = cmd_channel.log
        self.log_exception = cmd_channel.log_exception
        self._closed = False
        self._idler = None
        Acceptor.__init__(self, ioloop=cmd_channel.ioloop)

        local_ip = self.cmd_channel.socket.getsockname()[0]
        if local_ip in self.cmd_channel.masquerade_address_map:
            masqueraded_ip = self.cmd_channel.masquerade_address_map[local_ip]
        elif self.cmd_channel.masquerade_address:
            masqueraded_ip = self.cmd_channel.masquerade_address
        else:
            masqueraded_ip = None

        if self.cmd_channel.server._af != socket.AF_INET:
            # dual stack IPv4/IPv6 support
            af = self.bind_af_unspecified((local_ip, 0))
            self.socket.close()
        else:
            af = self.cmd_channel._af

        self.create_socket(af, socket.SOCK_STREAM)

        if self.cmd_channel.passive_ports is None:
            # By using 0 as port number value we let kernel choose a
            # free unprivileged random port.
            self.bind((local_ip, 0))
        else:
            ports = list(self.cmd_channel.passive_ports)
            while ports:
                port = ports.pop(random.randint(0, len(ports) - 1))
                self.set_reuse_addr()
                try:
                    self.bind((local_ip, port))
                except socket.error:
                    err = sys.exc_info()[1]
                    if err.args[0] == errno.EADDRINUSE:  # port already in use
                        if ports:
                            continue
                        # If cannot use one of the ports in the configured
                        # range we'll use a kernel-assigned port, and log
                        # a message reporting the issue.
                        # By using 0 as port number value we let kernel
                        # choose a free unprivileged random port.
                        else:
                            self.bind((local_ip, 0))
                            self.cmd_channel.log(
                                "Can't find a valid passive port in the "
                                "configured range. A random kernel-assigned "
                                "port will be used.",
                                logfun=logger.warning
                            )
                    else:
                        raise
                else:
                    break
        self.listen(self.backlog or self.cmd_channel.server.backlog)

        port = self.socket.getsockname()[1]
        if not extmode:
            ip = masqueraded_ip or local_ip
            if ip.startswith('::ffff:'):
                # In this scenario, the server has an IPv6 socket, but
                # the remote client is using IPv4 and its address is
                # represented as an IPv4-mapped IPv6 address which
                # looks like this ::ffff:151.12.5.65, see:
                # http://en.wikipedia.org/wiki/IPv6#IPv4-mapped_addresses
                # http://tools.ietf.org/html/rfc3493.html#section-3.7
                # We truncate the first bytes to make it look like a
                # common IPv4 address.
                ip = ip[7:]
            # The format of 227 response in not standardized.
            # This is the most expected:
            self.cmd_channel.respond('227 Entering passive mode (%s,%d,%d).' % (
                                ip.replace('.', ','), port // 256, port % 256))
        else:
            self.cmd_channel.respond('229 Entering extended passive mode '
                                     '(|||%d|).' % port)
        if self.timeout:
            self._idler = self.ioloop.call_later(self.timeout,
                                                 self.handle_timeout,
                                                 _errback=self.handle_error)

    # --- connection / overridden

    def handle_accepted(self, sock, addr):
        """Called when remote client initiates a connection."""
        if not self.cmd_channel.connected:
            return self.close()

        # Check the origin of data connection.  If not expressively
        # configured we drop the incoming data connection if remote
        # IP address does not match the client's IP address.
        if self.cmd_channel.remote_ip != addr[0]:
            if not self.cmd_channel.permit_foreign_addresses:
                try:
                    sock.close()
                except socket.error:
                    pass
                msg = '425 Rejected data connection from foreign address %s:%s.' \
                        %(addr[0], addr[1])
                self.cmd_channel.respond_w_warning(msg)
                # do not close listening socket: it couldn't be client's blame
                return
            else:
                # site-to-site FTP allowed
                msg = 'Established data connection with foreign address %s:%s.'\
                        % (addr[0], addr[1])
                self.cmd_channel.log(msg, logfun=logger.warning)
        # Immediately close the current channel (we accept only one
        # connection at time) and avoid running out of max connections
        # limit.
        self.close()
        # delegate such connection to DTP handler
        if self.cmd_channel.connected:
            handler = self.cmd_channel.dtp_handler(sock, self.cmd_channel)
            if handler.connected:
                self.cmd_channel.data_channel = handler
                self.cmd_channel._on_dtp_connection()

    def handle_timeout(self):
        if self.cmd_channel.connected:
            self.cmd_channel.respond("421 Passive data channel timed out.",
                                     logfun=logging.info)
        self.close()

    def handle_error(self):
        """Called to handle any uncaught exceptions."""
        try:
            raise
        except Exception:
            logger.error(traceback.format_exc())
        try:
            self.close()
        except Exception:
            logger.critical(traceback.format_exc())

    def close(self):
        if not self._closed:
            self._closed = True
            Acceptor.close(self)
            if self._idler is not None and not self._idler.cancelled:
                self._idler.cancel()


#Class FTPHandler

def ftp_FEAT(self, line):
    """List all new features supported as defined in RFC-2398."""
    features = set(['UTF8', 'TVFS'])
    features.update([feat for feat in ('EPRT', 'EPSV', 'MDTM', 'SIZE') \
                     if feat in self.proto_cmds])
    features.update(self._extra_feats)
    if 'MLST' in self.proto_cmds or 'MLSD' in self.proto_cmds:
        facts = ''
        for fact in self._available_facts:
            if fact in self._current_facts:
                facts += fact + '*;'
            else:
                facts += fact + ';'
        features.add('MLST ' + facts)
    if 'REST' in self.proto_cmds:
        features.add('REST STREAM')
        features = sorted(features)
        self.push("211-Features supported:\r\n")
        self.push("".join([" %s\r\n" % x for x in features]))
        self.respond('211 End FEAT.')
                    

#ioloop.py

# if select module has attribute "epoll" (i.e. we are on Linux), the
# class Epoll is defined in ioloop and has fileno method

def fileno(self):
    """Return epoll() fd."""
    return self._poller.fileno()


#servers.py

#Class FTPServer

def __init__(self, address_or_socket, handler, ioloop=None, backlog=5):
    """Creates a socket listening on 'address' dispatching
    connections to a 'handler'.
    
    - (tuple) address_or_socket: the (host, port) pair on which
    the command channel will listen for incoming connections or
    an existent socket object.
    
    - (instance) handler: the handler class to use.
    
    - (instance) ioloop: a pyftpdlib.ioloop.IOLoop instance
    
    - (int) backlog: the maximum number of queued connections
    passed to listen(). If a connection request arrives when
    the queue is full the client may raise ECONNRESET.
    Defaults to 5.
    """
    Acceptor.__init__(self, ioloop=ioloop)
    self.handler = handler
    self.backlog = backlog
    self.ip_map = []
    # in case of FTPS class not properly configured we want errors
    # to be raised here rather than later, when client connects
    if hasattr(handler, 'get_ssl_context'):
        handler.get_ssl_context()
    if isinstance(address_or_socket, socket.socket):
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

#class _SpawnerBase

from pyftpdlib.ioloop import IOLoop

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
        try:
            self._active_tasks.remove(self._current_task())
        except ValueError:
            pass
        ioloop.close()



# Updating code
################

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *
from pymoult.highlevel.managers import *
import sys


handlers = sys.modules['pyftpdlib.handlers']

#Update class PassiveDTP

#empty tranformer

def empty_transformer(obj):
    pass


class PassiveDTPUpdate(EagerConversionUpdate):
    def __init__(self,name):
        super(PassiveDTPUpdate,self).__init__(handlers.PassiveDTP,PassiveDTP,empty_transformer,name)

    def apply(self):
        redefineClass(handlers,handlers.PassiveDTP,PassiveDTP)
        super(PassiveDTPUpdate,self).apply()

passiveDTPup = PassiveDTPUpdate("passiveDTP")

        
#Update FTPHandler

ftpHandlerup = SafeRedefineMethodUpdate(handlers.FTPHandler,handlers.FTPHandler.ftp_FEAT,ftp_FEAT,"FTPHandler")

# ioloop.py

ioloop = sys.modules['pyftpdlib.ioloop']

if hasattr(ioloop,"Epoll"):
    class EpollUpdate(Update):
        def wait_alterability(self):
            return True
        
        def apply(self):
            addMethodToClass(ioloop.Epoll,"fileno",fileno)

    epollUp= EpollUpdate(name="epoll")

#servers

servers = sys.modules['pyftpdlib.servers']

#FTPServer

def ftpServerTransformer(obj):
    #Set backlog to default value: 5
    obj.backlog = 5


ftpServer1 = SafeRedefineMethodUpdate(servers.FTPServer,servers.FTPServer.__init__,__init__,"FTPServer1")

ftpServer2 = EagerConversionUpdate(servers.FTPServer,servers.FTPServer,ftpServerTransformer,"FTPServer2")

#class _SpawnerBase

spawner = SafeRedefineMethodUpdate(servers._SpawnerBase,servers._SpawnerBase._loop,_loop,"SpawnerBase")



#Create a manager

manager = ThreadedManager("manager")
manager.start()


manager.add_update(passiveDTPup)
manager.add_update(ftpHandlerup)
if hasattr(ioloop,"Epoll"):
    manager.add_update(epollUp)
manager.add_update(ftpServer1)
manager.add_update(ftpServer1)
manager.add_update(spawner)


