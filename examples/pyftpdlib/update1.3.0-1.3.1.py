#parsed

############################################################
#
# Pymoult dynamic patch for pyftpdlib v1.3.0 to v1.3.1
#
############################################################

# New code
###########

import logging
import curses
from pyftpdlib._compat import unicode, PY3
import os
import sys
import time
from tarfile import filemode as _filemode

filesystems = sys.modules["pyftpdlib.filesystems"]

#Filsystems
#Class AbstractedFS

def format_list(self, basedir, listing, ignore_err=True):
    assert isinstance(basedir, unicode), basedir
    if listing:
        assert isinstance(listing[0], unicode)
    if self.cmd_channel.use_gmt_times:
        timefunc = time.gmtime
    else:
        timefunc = time.localtime
    SIX_MONTHS = 180 * 24 * 60 * 60
    readlink = getattr(self, 'readlink', None)
    now = time.time()
    for basename in listing:
        if not PY3:
            try:
                file = os.path.join(basedir, basename)
            except UnicodeDecodeError:
                file = os.path.join(bytes(basedir), bytes(basename))
                if not isinstance(basename, unicode):
                    basename = unicode(basename, 'utf8', 'ignore')
        else:
            file = os.path.join(basedir, basename)
        try:
            st = self.lstat(file)
        except (OSError, FilesystemError):
            if ignore_err:
                continue
            raise

        perms = _filemode(st.st_mode)  # permissions
        nlinks = st.st_nlink  # number of links to inode
        if not nlinks:  # non-posix system, let's use a bogus value
            nlinks = 1
        size = st.st_size  # file size
        uname = self.get_user_by_uid(st.st_uid)
        gname = self.get_group_by_gid(st.st_gid)
        mtime = timefunc(st.st_mtime)
        # if modification time > 6 months shows "month year"
        # else "month hh:mm";  this matches proftpd format, see:
        # http://code.google.com/p/pyftpdlib/issues/detail?id=187
        if (now - st.st_mtime) > SIX_MONTHS:
            fmtstr = "%d  %Y"
        else:
            fmtstr = "%d %H:%M"
        try:
            mtimestr = "%s %s" % (filesystems._months_map[mtime.tm_mon],
                                  time.strftime(fmtstr, mtime))
        except ValueError:
            # It could be raised if last mtime happens to be too
            # old (prior to year 1900) in which case we return
            # the current time as last mtime.
            mtime = timefunc()
            mtimestr = "%s %s" % (filesystems._months_map[mtime.tm_mon],
                                  time.strftime("%d %H:%M", mtime))

        # same as stat.S_ISLNK(st.st_mode) but slighlty faster
        islink = (st.st_mode & 61440) == stat.S_IFLNK
        if islink and readlink is not None:
            # if the file is a symlink, resolve it, e.g.
            # "symlink -> realfile"
            try:
                basename = basename + " -> " + readlink(file)
            except (OSError, FilesystemError):
                if not ignore_err:
                    raise

        # formatting is matched with proftpd ls output
        line = "%s %3s %-8s %-8s %8s %s %s\r\n" % (
            perms, nlinks, uname, gname, size, mtimestr, basename)
        yield line.encode('utf8', self.cmd_channel.unicode_errors)

        
def format_mlsx(self, basedir, listing, perms, facts, ignore_err=True):
    assert isinstance(basedir, unicode), basedir
    if listing:
        assert isinstance(listing[0], unicode)
    if self.cmd_channel.use_gmt_times:
        timefunc = time.gmtime
    else:
        timefunc = time.localtime
    permdir = ''.join([x for x in perms if x not in 'arw'])
    permfile = ''.join([x for x in perms if x not in 'celmp'])
    if ('w' in perms) or ('a' in perms) or ('f' in perms):
        permdir += 'c'
    if 'd' in perms:
        permdir += 'p'
    show_type = 'type' in facts
    show_perm = 'perm' in facts
    show_size = 'size' in facts
    show_modify = 'modify' in facts
    show_create = 'create' in facts
    show_mode = 'unix.mode' in facts
    show_uid = 'unix.uid' in facts
    show_gid = 'unix.gid' in facts
    show_unique = 'unique' in facts
    for basename in listing:
        retfacts = dict()
        if not PY3:
            try:
                file = os.path.join(basedir, basename)
            except UnicodeDecodeError:
                # (Python 2 only) might happen on filesystem not
                # supporting UTF8 meaning os.listdir() returned a list
                # of mixed bytes and unicode strings:
                # http://goo.gl/6DLHD
                # http://bugs.python.org/issue683592
                file = os.path.join(bytes(basedir), bytes(basename))
                if not isinstance(basename, unicode):
                    basename = unicode(basename, 'utf8', 'ignore')
        else:
            file = os.path.join(basedir, basename)
        # in order to properly implement 'unique' fact (RFC-3659,
        # chapter 7.5.2) we are supposed to follow symlinks, hence
        # use os.stat() instead of os.lstat()
        try:
            st = self.stat(file)
        except (OSError, FilesystemError):
            if ignore_err:
                continue
            raise
        # type + perm
        # same as stat.S_ISDIR(st.st_mode) but slightly faster
        isdir = (st.st_mode & 61440) == stat.S_IFDIR
        if isdir:
            if show_type:
                if basename == '.':
                    retfacts['type'] = 'cdir'
                elif basename == '..':
                    retfacts['type'] = 'pdir'
                else:
                    retfacts['type'] = 'dir'
            if show_perm:
                retfacts['perm'] = permdir
        else:
            if show_type:
                retfacts['type'] = 'file'
            if show_perm:
                retfacts['perm'] = permfile
        if show_size:
            retfacts['size'] = st.st_size  # file size
        # last modification time
        if show_modify:
            try:
                retfacts['modify'] = time.strftime("%Y%m%d%H%M%S",
                                                   timefunc(st.st_mtime))
            # it could be raised if last mtime happens to be too old
            # (prior to year 1900)
            except ValueError:
                pass
        if show_create:
            # on Windows we can provide also the creation time
            try:
                retfacts['create'] = time.strftime("%Y%m%d%H%M%S",
                                                   timefunc(st.st_ctime))
            except ValueError:
                pass
        # UNIX only
        if show_mode:
            retfacts['unix.mode'] = oct(st.st_mode & 511)
        if show_uid:
            retfacts['unix.uid'] = st.st_uid
        if show_gid:
            retfacts['unix.gid'] = st.st_gid

        # We provide unique fact (see RFC-3659, chapter 7.5.2) on
        # posix platforms only; we get it by mixing st_dev and
        # st_ino values which should be enough for granting an
        # uniqueness for the file listed.
        # The same approach is used by pure-ftpd.
        # Implementors who want to provide unique fact on other
        # platforms should use some platform-specific method (e.g.
        # on Windows NTFS filesystems MTF records could be used).
        if show_unique:
            retfacts['unique'] = "%xg%x" % (st.st_dev, st.st_ino)

        # facts can be in any order but we sort them by name
        factstring = "".join(["%s=%s;" % (x, retfacts[x])
                              for x in sorted(retfacts.keys())])
        line = "%s %s\r\n" % (factstring, basename)
        yield line.encode('utf8', self.cmd_channel.unicode_errors)

#handlers.py
#class SSLConnection

def _do_ssl_shutdown(self):
    """Executes a SSL_shutdown() call to revert the connection
    back to clear-text.
    twisted/internet/tcp.py code has been used as an example.
    """
    self._ssl_closing = True
    if os.name == 'posix':
        # since SSL_shutdown() doesn't report errors, an empty
        # write call is done first, to try to detect if the
        # connection has gone away
        try:
            os.write(self.socket.fileno(), b(''))
        except (OSError, socket.error):
            err = sys.exc_info()[1]
            if err.args[0] in (errno.EINTR, errno.EWOULDBLOCK,
                               errno.ENOBUFS):
                return
            elif err.args[0] in _DISCONNECTED:
                return super(SSLConnection, self).close()
            else:
                raise
    # Ok, this a mess, but the underlying OpenSSL API simply
    # *SUCKS* and I really couldn't do any better.
    #
    # Here we just want to shutdown() the SSL layer and then
    # close() the connection so we're not interested in a
    # complete SSL shutdown() handshake, so let's pretend
    # we already received a "RECEIVED" shutdown notification
    # from the client.
    # Once the client received our "SENT" shutdown notification
    # then we close() the connection.
    #
    # Since it is not clear what errors to expect during the
    # entire procedure we catch them all and assume the
    # following:
    # - WantReadError and WantWriteError means "retry"
    # - ZeroReturnError, SysCallError[EOF], Error[] are all
    #   aliases for disconnection
    try:
        laststate = self.socket.get_shutdown()
        self.socket.set_shutdown(laststate | SSL.RECEIVED_SHUTDOWN)
        done = self.socket.shutdown()
        if not (laststate & SSL.RECEIVED_SHUTDOWN):
            self.socket.set_shutdown(SSL.SENT_SHUTDOWN)
    except (SSL.WantReadError, SSL.WantWriteError):
        pass
    except SSL.ZeroReturnError:
        super(SSLConnection, self).close()
    except SSL.SysCallError:
        err = sys.exc_info()[1]
        errnum, errstr = err.args
        if errnum in _DISCONNECTED or errstr == 'Unexpected EOF':
            super(SSLConnection, self).close()
        else:
            raise
    except SSL.Error:
        # see:
        # http://code.google.com/p/pyftpdlib/issues/detail?id=171
        # https://bugs.launchpad.net/pyopenssl/+bug/785985
        err = sys.exc_info()[1]
        if err.args and not err.args[0]:
            pass
        else:
            raise
    except socket.error:
        err = sys.exc_info()[1]
        if err.args[0] in _DISCONNECTED:
            super(SSLConnection, self).close()
        else:
            raise
    else:
        if done:
            self._ssl_established = False
            self._ssl_closing = False
            self.handle_ssl_shutdown()

#TLS_FTPHandler
#classmethod
def get_ssl_context(cls):
    if cls.ssl_context is None:
        if cls.certfile is None:
            raise ValueError("at least certfile must be specified")
        cls.ssl_context = SSL.Context(cls.ssl_protocol)
        if cls.ssl_protocol != SSL.SSLv2_METHOD:
            cls.ssl_context.set_options(SSL.OP_NO_SSLv2)
        else:
            warnings.warn("SSLv2 protocol is insecure", RuntimeWarning)
        cls.ssl_context.use_certificate_chain_file(cls.certfile)
        if not cls.keyfile:
            cls.keyfile = cls.certfile
        cls.ssl_context.use_privatekey_file(cls.keyfile)
    return cls.ssl_context


#ioloop
#class _IOLoop

ioloop = sys.modules["pyftpdlib.ioloop"]
log = sys.modules["pyftpdlib.log"]


def loop(self, timeout=None, blocking=True):
    if not ioloop._IOLoop._started_once:
        _IOLoop._started_once = True
        if not logging.getLogger('pyftpdlib').handlers:
            # If we get to this point it means the user hasn't
            # configured logging. We want to log by default so
            # we configure logging ourselves so that it will
            # print to stderr.
            log._config_logging()

    if blocking:
        # localize variable access to minimize overhead
        poll = self.poll
        socket_map = self.socket_map
        sched_poll = self.sched.poll

        if timeout is not None:
            while socket_map:
                poll(timeout)
                sched_poll()
        else:
            soonest_timeout = None
            while socket_map:
                poll(soonest_timeout)
                soonest_timeout = sched_poll()
    else:
        sched = self.sched
        if self.socket_map:
            self.poll(timeout)
        if sched._tasks:
            return sched.poll()

#log.py
#class LogFormatter

def __init__(self, *args, **kwargs):
    logging.Formatter.__init__(self, *args, **kwargs)
    self._coloured = COLOURED and _stderr_supports_color()
    if self._coloured:
        curses.setupterm()
        # The curses module has some str/bytes confusion in
        # python3.  Until version 3.2.3, most methods return
        # bytes, but only accept strings.  In addition, we want to
        # output these strings with the logging module, which
        # works with unicode strings.  The explicit calls to
        # unicode() below are harmless in python2 but will do the
        # right conversion in python 3.
        fg_color = (curses.tigetstr("setaf") or curses.tigetstr("setf")
                    or "")
        if (3, 0) < sys.version_info < (3, 2, 3):
            fg_color = unicode(fg_color, "ascii")
        self._colors = {
            # blues
            logging.DEBUG: unicode(curses.tparm(fg_color, 4), "ascii"),
            # green
            logging.INFO: unicode(curses.tparm(fg_color, 2), "ascii"),
            # yellow
            logging.WARNING: unicode(curses.tparm(fg_color, 3), "ascii"),
            # red
            logging.ERROR: unicode(curses.tparm(fg_color, 1), "ascii")
        }
        self._normal = unicode(curses.tigetstr("sgr0"), "ascii")

#transformer : change self._colors

def _config_logging():
    channel = logging.StreamHandler()
    channel.setFormatter(LogFormatter())
    logger = logging.getLogger('pyftpdlib')
    logger.setLevel(LEVEL)
    logger.addHandler(channel)

#servers

#class FTPServer

def _log_start(self):
    if not logging.getLogger('pyftpdlib').handlers:
        # If we get to this point it means the user hasn't
        # configured logger. We want to log by default so
        # we configure logging ourselves so that it will
        # print to stderr.
        from pyftpdlib.ioloop import _config_logging
        _config_logging()

    if self.handler.passive_ports:
        pasv_ports = "%s->%s" % (self.handler.passive_ports[0],
                                 self.handler.passive_ports[-1])
    else:
        pasv_ports = None
    addr = self.address
    logger.info(">>> starting FTP server on %s:%s, pid=%i <<<"
                % (addr[0], addr[1], os.getpid()))
    logger.info("poller: %r", self.ioloop.__class__)
    logger.info("masquerade (NAT) address: %s",
                self.handler.masquerade_address)
    logger.info("passive ports: %s", pasv_ports)
    if os.name == 'posix':
        logger.info("use sendfile(2): %s", self.handler.use_sendfile)

# Updating code
################

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *
from pymoult.highlevel.managers import *
from pymoult.threads import *

#filesystems

filesystems = sys.modules["pyftpdlib.filesystems"]

abstracted1up = SafeRedefineMethodUpdate(filesystems.AbstractedFS,filesystems.AbstractedFS.format_list,format_list,name="abstracted1")

abstracted2up = SafeRedefineMethodUpdate(filesystems.AbstractedFS,filesystems.AbstractedFS.format_mlsx,format_mlsx,name="abstracted2")


#handlers

handlers = sys.modules["pyftpdlib.handlers"]

if hasattr(handlers,"SSLConnection"):
    sslconnection1up = SafeRedefineMethodUpdate(handlers.SSLConnection,handlers.SSLConnection._do_ssl_shutdown,_do_ssl_shutdown,name="sslconnection1")
    tlsftp1up = SafeRedefineMethodUpdate(handlers.TLS_FTPHandler,handlers.TLS_FTPHandler.get_ssl_context,get_ssl_context,name="tlsftp1")

#iloop

ioloop = sys.modules["pyftpdlib.ioloop"]

mainThread = get_thread_by_name("mainThread")

import time
class IoLoopUpdate(Update):
    def __init__(self,name):
        super(IoLoopUpdate,self).__init__(name=name)
    
    def wait_alterability(self):
        #We want to reboot the thread only when loop is at the top of
        #the stack or when the thread is stuck at poll.
        tries = 0
        while tries <= self.max_tries:
            mainThread.suspend()
            mainThread.wait_suspended(timeout=3)
            stack = get_current_frames()[mainThread.ident]
            if stack.f_code == ioloop._IOLoop.loop.__code__ or stack.f_code.co_name == "poll":
                return True
            mainThread.resume()
            tries+=1
            time.sleep(self.sleep_time)
        return False

    def apply(self):
        addMethodToClass(ioloop._IOLoop,"loop",loop)
        resetThread(mainThread)

    def resume_hook(self):
        mainThread.resume()

ioloop1up = IoLoopUpdate("ioloop1")
ioloop1up.set_sleep_time(0.2)

#logs

log = sys.modules["pyftpdlib.log"]

logFormatter1up = SafeRedefineMethodUpdate(log.LogFormatter,log.LogFormatter.__init__,__init__,name="logFormatter1") 


fg_color = (curses.tigetstr("setaf") or curses.tigetstr("setf") or "")

def transformer(obj):
    obj._colors = {
        # blues
        logging.DEBUG: unicode(curses.tparm(fg_color, 4), "ascii"),
        # green
        logging.INFO: unicode(curses.tparm(fg_color, 2), "ascii"),
        # yellow
        logging.WARNING: unicode(curses.tparm(fg_color, 3), "ascii"),
        # red
        logging.ERROR: unicode(curses.tparm(fg_color, 1), "ascii")
    }
    
logFormatter2up = EagerConversionUpdate(log.LogFormatter,log.LogFormatter,transformer,"logFormatter2")

configLoggingUp = SafeRedefineUpdate(log,log._config_logging,_config_logging,name="configLogging1")

#servers
servers = sys.modules["pyftpdlib.servers"]

ftpServer1up = SafeRedefineMethodUpdate(servers.FTPServer,servers.FTPServer._log_start,_log_start,name="ftpServer1") 

#Fetch manager

manager = fetch_manager("manager")


manager.add_update(abstracted1up)
manager.add_update(abstracted2up)
if hasattr(handlers,"SSLConnection"):
    manager.add_update(sslconnection1up)
    manager.add_update(tlsftp1up)
manager.add_update(ioloop1up)
manager.add_update(logFormatter1up)
manager.add_update(logFormatter2up)
manager.add_update(configLoggingUp)
manager.add_update(ftpServer1up)

