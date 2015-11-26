#django.db.backend.mysql.schema
import sys

schema = sys.modules['django.db.backend.mysql.schema']

#Class DatabaseSchemaEditor
def _alter_column_type_sql(self, table, old_field, new_field, new_type):
    # Keep null property of old field, if it has changed, it will be handled separately
    if old_field.null:
        new_type += " NULL"
    else:
        new_type += " NOT NULL"
    return super(DatabaseSchemaEditor, self)._alter_column_type_sql(table, old_field, new_field, new_type)


from pymoult.highlevel.updates import *

msUpdate = SafeRedefineMethodUpdate(schema._alter_column_type_sql,schema._alter_column_type_sql,_alter_column_type_sql,"_alter_column_type_sql")


