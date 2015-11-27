#django.db.backends.base.creation
import sys

creation = sys.modules['django.db.backends.base.creation']

#class BaseDatabaseCreation
def _destroy_test_db(self, test_database_name, verbosity):
      """
      Internal implementation - remove the test db tables.
      """
      # Remove the test database to clean up after
      # ourselves. Connect to the previous database (not the test database)
      # to do so, because it's not allowed to delete a database while being
      # connected to it.
      with self.connection._nodb_connection.cursor() as cursor:
          # Wait to avoid "database is being accessed by other users" errors.
          time.sleep(1)
          cursor.execute("DROP DATABASE %s"
                         % self.connection.ops.quote_name(test_database_name))


from pymoult.highlevel.updates import *

cUpdate = SafeRedefineMethodUpdate(creation.BaseDatabaseCreation,creation.BaseDatabaseCreation._destroy_test_db,_destroy_test_db)



    


