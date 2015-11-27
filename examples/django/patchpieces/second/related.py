#django.db.models.fields.related
import sys

related = sys.modules['django.db.models.fields.related']

#class ForeignKey
def get_db_prep_value(self, value, connection, prepared=False):
      return self.related_field.get_db_prep_value(value, connection, prepared)


from pymoult.highlevel.updates import *

rUpdate = SafeRedefineMethodUpdate(related.ForeignKey,related.ForeignKey.get_db_prep_value,get_db_prep_value)



    


