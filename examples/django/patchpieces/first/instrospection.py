#django.db.backends.sqlite3.introspection

import sys

introspec = sys.modules['django.db.backends.sqlite3.introspection']

#class DatabaseIntrospection
def get_constraints(self, cursor, table_name):
    """
    Retrieves any constraints or keys (unique, pk, fk, check, index) across one or more columns.
    """
    constraints = {}
    # Get the index info
    cursor.execute("PRAGMA index_list(%s)" % self.connection.ops.quote_name(table_name))
    for row in cursor.fetchall():
        # Sqlite3 3.8.9+ has 5 columns, however older versions only give 3
        # columns. Discard last 2 columns if there.
        number, index, unique = row[:3]
        # Get the index info for that index
        cursor.execute('PRAGMA index_info(%s)' % self.connection.ops.quote_name(index))
        for index_rank, column_rank, column in cursor.fetchall():
            if index not in constraints:
                constraints[index] = {
                    "columns": [],
                    "primary_key": False,
                    "unique": bool(unique),
                    "foreign_key": False,
                    "check": False,
                    "index": True,
                }
            constraints[index]['columns'].append(column)
    # Get the PK
    pk_column = self.get_primary_key_column(cursor, table_name)
    if pk_column:
        # SQLite doesn't actually give a name to the PK constraint,
        # so we invent one. This is fine, as the SQLite backend never
        # deletes PK constraints by name, as you can't delete constraints
        # in SQLite; we remake the table with a new PK instead.
        constraints["__primary__"] = {
            "columns": [pk_column],
            "primary_key": True,
            "unique": False,  # It's not actually a unique constraint.
            "foreign_key": False,
            "check": False,
            "index": False,
        }
    return constraints



from pymoult.highlevel.updates import *

iUpdate = SafeRedefineMethodUpdate(introspec.DatabaseIntrospection,introspec.DatabaseIntrospection.get_constraints,get_constraints,"get_constraints")



    


