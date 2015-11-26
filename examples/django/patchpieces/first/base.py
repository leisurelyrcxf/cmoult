#django.models.base

import sys

base = sys.modules['django.models.base']

#Class Model
def prepare_database_save(self, field):
    if self.pk is None:
        raise ValueError("Unsaved model instance %r cannot be used in an ORM query." % self)
    return getattr(self, field.rel.get_related_field().attname)

from pymoult.highlevel.updates import *

bUpdate = SafeRedefineMethodUpdate(base.Model,base.Model.prepare_database_save)


