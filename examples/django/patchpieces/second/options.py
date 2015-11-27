#django.contrib.gis.admin.options
from django.core.exceptions import ImproperlyConfigured
import sys

options = sys.modules['django.contrib.gis.admin.options']

class OSMGeoAdmin(GeoModelAdmin):
    map_template = 'gis/admin/osm.html'
    num_zoom = 20
    map_srid = spherical_mercator_srid
    max_extent = '-20037508,-20037508,20037508,20037508'
    max_resolution = '156543.0339'
    point_zoom = num_zoom - 6
    units = 'm'

    def __init__(self, *args):
        if not HAS_GDAL:
            raise ImproperlyConfigured("OSMGeoAdmin is not usable without GDAL libs installed")
        super(OSMGeoAdmin, self).__init__(*args)


from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *


class OptionsUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        redefineClass(options,otpions.OSMGeoAdminschema,OSMGeoAdminschema)
        options.spherical_mercator_srid = 3857




oUpdate = OptionsUpdate()


