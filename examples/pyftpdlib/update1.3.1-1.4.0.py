#parsed

############################################################
#
# Pymoult dynamic patch for pyftpdlib v1.3.1 to v1.4.0
#
############################################################

# New code
###########

#handlers

#class SSLConnection (may not exist)

def send(self, data):
    if not isinstance(data, bytes):
        data = bytes(data)
    try:
        return super(SSLConnection, self).send(data)
    except (SSL.WantReadError, SSL.WantWriteError):
        return 0
    except SSL.ZeroReturnError:
        super(SSLConnection, self).handle_close()
        return 0
    except SSL.SysCallError:
        err = sys.exc_info()[1]
        errnum, errstr = err.args
        if errnum == errno.EWOULDBLOCK:
            return 0
        elif errnum in _DISCONNECTED or errstr == 'Unexpected EOF':
            super(SSLConnection, self).handle_close()
            return 0
        else:
            raise


# Updating code
################

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *
from pymoult.highlevel.managers import *
import sys

#handlers

handlers = sys.modules["pyftpdlib.handlers"]

if hasattr(handlers,"SSLConnection"):
    sslUp = SafeRedefineMethodUpdate(handlers.SSLConnection,handlers.SSLConnection.send,send,name="sslUpdate")


#Fetch manager from previous update 

manager = fetch_manager("manager")

if hasattr(handlers,"SSLConnection"):
    manager.add_update(sslUp)




