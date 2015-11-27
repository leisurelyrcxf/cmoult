#django.contrib.gis.admin.__init__
from django.contrib.gis.admin.options import GeoModelAdmin, OSMGeoAdmin
from django.contrib.gis.admin.widgets import OpenLayersWidget


import sys

init = sys.modules['django.contrib.gis.admin.__init__']

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *

class InitUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        init.__all__ = ['autodiscover', 'site', 'AdminSite', 'ModelAdmin', 'StackedInline','TabularInline', 'HORIZONTAL', 'VERTICAL', 'GeoModelAdmin', 'OSMGeoAdmin','OpenLayersWidget']

        
iUpdate = initUpdate()


