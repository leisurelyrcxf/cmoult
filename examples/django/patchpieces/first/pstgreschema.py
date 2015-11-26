#django.db.backends.postgresql_psycopg2.schema

import sys

schema = sys.modules['django.db.backends.postgresql_psycopg2.schema']

#class DatabaseSchemaEditor

def _alter_column_type_sql(self, table, old_field, new_field, new_type):
    """
    Makes ALTER TYPE with SERIAL make sense.
    """
    if new_type.lower() == "serial":
        column = new_field.column
        sequence_name = "%s_%s_seq" % (table, column)
        return (
            (
                self.sql_alter_column_type % {
                    "column": self.quote_name(column),
                    "type": "integer",
                },
                [],
            ),
            [
                (
                    self.sql_delete_sequence % {
                        "sequence": sequence_name,
                    },
                    [],
                ),
                (
                    self.sql_create_sequence % {
                        "sequence": sequence_name,
                    },
                    [],
                ),
                (
                    self.sql_alter_column % {
                        "table": table,
                        "changes": self.sql_alter_column_default % {
                            "column": column,
                            "default": "nextval('%s')" % sequence_name,
                        }
                    },
                    [],
                ),
                (
                    self.sql_set_sequence_max % {
                        "table": table,
                        "column": column,
                        "sequence": sequence_name,
                    },
                    [],
                ),
            ],
        )
    else:
        return super(DatabaseSchemaEditor, self)._alter_column_type_sql(
            table, old_field, new_field, new_type
        )


from pymoult.highlevel.updates import *

psUpdate = SafeRedefineMethodUpdate(schema.DatabaseSchemaEditor,schema.DatabaseSchemaEditor._alter_column_type_sql,_alter_column_type_sql,"_alter_column_type_sql")



