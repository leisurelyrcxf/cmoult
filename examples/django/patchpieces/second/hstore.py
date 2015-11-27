#django.contrib.prostgres.fields.hstore
import sys

hstore = sys.modules['django.contrib.prostgres.fields.hstore']

class KeyTransform(Transform):
    output_field = TextField()

    def __init__(self, key_name, *args, **kwargs):
        super(KeyTransform, self).__init__(*args, **kwargs)
        self.key_name = key_name

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "(%s -> '%s')" % (lhs, self.key_name), params

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *


class HstoreUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        redefineClass(hstore,hstore.keytransform,Keytransform)

oUpdate = HstoreUpdate()


