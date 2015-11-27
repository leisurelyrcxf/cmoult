#django.db.backends.base.schema
import sys

schema = sys.modules['django.db.backends.base.schema']

#class BaseDatabaseSchemaEditor

def alter_unique_together(self, model, old_unique_together, new_unique_together):
    """
    Deals with a model changing its unique_together.
    Note: The input unique_togethers must be doubly-nested, not the single-
    nested ["foo", "bar"] format.
    """
    olds = set(tuple(fields) for fields in old_unique_together)
    news = set(tuple(fields) for fields in new_unique_together)
    # Deleted uniques
    for fields in olds.difference(news):
        self._delete_composed_index(model, fields, {'unique': True}, self.sql_delete_unique)
    # Created uniques
    for fields in news.difference(olds):
        columns = [model._meta.get_field(field).column for field in fields]
        self.execute(self._create_unique_sql(model, columns))

def alter_index_together(self, model, old_index_together, new_index_together):
    """
    Deals with a model changing its index_together.
    Note: The input index_togethers must be doubly-nested, not the single-
    nested ["foo", "bar"] format.
    """
    olds = set(tuple(fields) for fields in old_index_together)
    news = set(tuple(fields) for fields in new_index_together)
    # Deleted indexes
    for fields in olds.difference(news):
        self._delete_composed_index(model, fields, {'index': True}, self.sql_delete_index)
    # Created indexes
    for field_names in news.difference(olds):
        fields = [model._meta.get_field(field) for field in field_names]
        self.execute(self._create_index_sql(model, fields, suffix="_idx"))

def _delete_composed_index(self, model, fields, constraint_kwargs, sql):
    columns = [model._meta.get_field(field).column for field in fields]
    constraint_names = self._constraint_names(model, columns, **constraint_kwargs)
    if len(constraint_names) != 1:
        raise ValueError("Found wrong number (%s) of constraints for %s(%s)" % (
            len(constraint_names),
            model._meta.db_table,
            ", ".join(columns),
        ))
    self.execute(self._delete_constraint_sql(sql, model, constraint_names[0]))

from pymoult.highlevel.updates import *

sc1Update = SafeRedefineMethodUpdate(schema.BaseDatabaseSchemaEditor,schema.BaseDatabaseSchemaEditor.alter_unique_together,alter_unique_together)

sc2Update = SafeRedefineMethodUpdate(schema.BaseDatabaseSchemaEditor,schema.BaseDatabaseSchemaEditor.alter_index_together,alter_index_together)

sc3Update = SafeRedefineMethodUpdate(schema.BaseDatabaseSchemaEditor,schema.BaseDatabaseSchemaEditor._delete_composed_index,_delete_composed_index)



    


