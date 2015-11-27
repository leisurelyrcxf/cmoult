#django.contrib.sessions.backends.cached_db
import sys

cached = sys.modules['django.contrib.sessions.backends.cached_db']
#class SessionStore
def flush(self):
    """
    Removes the current session data from the database and regenerates the
    key.
    """
    self.clear()
    self.delete(self.session_key)
    self._session_key = None

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_access import *

class CachedUpdate(SafeRedefineMethodUpdate):
    def wait_alterability(self):
        return super(self,SafeRedefineMethodUpdate).wait_alterability()
    def apply(self):
        super(self,SafeRedefineMethodUpdate).apply()
        d= DataAccessor(self.cls)
        for item in d:
            if item._session_key == '':
                item._session_key = None

cUpdate = CachedUpdate(cached.SessionStore,cached.SessionStore.flush,flush)


