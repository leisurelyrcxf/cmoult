#django.db.backends.mysql.schema
import sys

schema = sys.modules['django.db.backends.mysql.schema']

#class DatabaseSchemaEditor
def _delete_composed_index(self, model, fields, *args):
      """
      MySQL can remove an implicit FK index on a field when that field is
      covered by another index like a unique_together. "covered" here means
      that the more complex index starts like the simpler one.
      http://bugs.mysql.com/bug.php?id=37910 / Django ticket #24757
      We check here before removing the [unique|index]_together if we have to
      recreate a FK index.
      """
      first_field = model._meta.get_field(fields[0])
      if first_field.get_internal_type() == 'ForeignKey':
          constraint_names = self._constraint_names(model, fields[0], index=True)
          if not constraint_names:
              self.execute(
                  self._create_index_sql(model, [model._meta.get_field(fields[0])], suffix="")
              )
      return super(DatabaseSchemaEditor, self)._delete_composed_index(model, fields, *args)


from pymoult.highlevel.updates import *
from.pymoult.lowlevel.data_update import *

class SchemUpdate(Update):
      def wait_alterability(self):
            return True
      def apply(self):
            addMethodToClass(schema.DatabaseSchemaEditor,"_delete_composed_index",_delete_composed_index)

scUpdate = SchemUpdate()



    


