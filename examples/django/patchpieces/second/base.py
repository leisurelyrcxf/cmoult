#django.db.backends.postgresql_psycopg2.base
import sys

#import warnings
#from django.db import DEFAULT_DB_ALIAS
#from django.db.utils import DatabaseError as WrappedDatabaseError

base = sys.modules['django.db.backends.postgresql_psycopg2.base']

#class DatabaseWrapper
@cached_property
def _nodb_connection(self):
    nodb_connection = super(DatabaseWrapper, self)._nodb_connection
    try:
        nodb_connection.ensure_connection()
    except (DatabaseError, WrappedDatabaseError):
        warnings.warn(
            "Normally Django will use a connection to the 'postgres' database "
            "to avoid running initialization queries against the production "
            "database when it's not needed (for example, when running tests). "
            "Django was unable to create a connection to the 'postgres' database "
            "and will use the default database instead.",
            RuntimeWarning
        )
        settings_dict = self.settings_dict.copy()
        settings_dict['NAME'] = settings.DATABASES[DEFAULT_DB_ALIAS]['NAME']
        nodb_connection = self.__class__(
            self.settings_dict.copy(),
            alias=self.alias,
            allow_thread_sharing=False)
    return nodb_connection



from pymoult.highlevel.updates import *

bUpdate = SafeRedefineMethodUpdate(base.DatabaseWrapper,base.DatabaseWrapper._nodb_connection,_nodb_connection)



    


