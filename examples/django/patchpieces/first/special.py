#django.db.migrations.operations.special

import sys

special = sys.modules['django.db.migrations.operations.special']

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *

class SpecialUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        special.SeparateDatabaseAndState.serialization_expand_args = ['database_operations', 'state_operations']


speUpdate = SpecialUpdate()


