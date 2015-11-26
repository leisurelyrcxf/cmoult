#django.contrib.gis.gdal.prototypes.raster
from ctypes import POINTER, c_char_p, c_double, c_int, c_void_p
from functools import partial

from django.contrib.gis.gdal.libgdal import std_call
from django.contrib.gis.gdal.prototypes.generation import (
    const_string_output, double_output, int_output, void_output,
    voidptr_output,
)

import sys

raster = sys.modules['django.contrib.gis.gdal.prototypes.raster']

from pymoult.highlevel.updates import *
from pymoult.lowlevel.data_update import *

class RasterUpdate(Update):
    def wait_alterability(self):
        return True
    def apply(self):
        raster.register_all = void_output(std_call('GDALAllRegister'), [])
        raster.get_driver = voidptr_output(std_call('GDALGetDriver'), [c_int])
        raster.get_driver_by_name = voidptr_output(std_call('GDALGetDriverByName'), [c_char_p], errcheck=False)
        raster.get_driver_count = int_output(std_call('GDALGetDriverCount'), [])
        raster.get_driver_description = const_string_output(std_call('GDALGetDescription'), [c_void_p])

        raster.create_ds = voidptr_output(std_call('GDALCreate'), [c_void_p, c_char_p, c_int, c_int, c_int, c_int, c_void_p])
        raster.open_ds = voidptr_output(std_call('GDALOpen'), [c_char_p, c_int])
        raster.close_ds = void_output(std_call('GDALClose'), [c_void_p])
        raster.copy_ds = voidptr_output(std_call('GDALCreateCopy'),[c_void_p, c_char_p, c_void_p, c_int, POINTER(c_char_p), c_void_p, c_void_p])
        raster.add_band_ds = void_output(std_call('GDALAddBand'), [c_void_p, c_int])
        raster.get_ds_description = const_string_output(std_call('GDALGetDescription'), [c_void_p])
        raster.get_ds_driver = voidptr_output(std_call('GDALGetDatasetDriver'), [c_void_p])
        raster.get_ds_xsize = int_output(std_call('GDALGetRasterXSize'), [c_void_p])
        raster.get_ds_ysize = int_output(std_call('GDALGetRasterYSize'), [c_void_p])
        raster.get_ds_raster_count = int_output(std_call('GDALGetRasterCount'), [c_void_p])
        raster.get_ds_raster_band = voidptr_output(std_call('GDALGetRasterBand'), [c_void_p, c_int])
        raster.get_ds_projection_ref = const_string_output(std_call('GDALGetProjectionRef'), [c_void_p])
        raster.set_ds_projection_ref = void_output(std_call('GDALSetProjection'), [c_void_p, c_char_p])
        raster.get_ds_geotransform = void_output(std_call('GDALGetGeoTransform'), [c_void_p, POINTER(c_double * 6)], errcheck=False)
        raster.set_ds_geotransform = void_output(std_call('GDALSetGeoTransform'), [c_void_p, POINTER(c_double * 6)])
        
        raster.band_io = void_output(std_call('GDALRasterIO'),[c_void_p, c_int, c_int, c_int, c_int, c_int, c_void_p, c_int, c_int, c_int, c_int, c_int])
        raster.get_band_xsize = int_output(std_call('GDALGetRasterBandXSize'), [c_void_p])
        raster.get_band_ysize = int_output(std_call('GDALGetRasterBandYSize'), [c_void_p])
        raster.get_band_index = int_output(std_call('GDALGetBandNumber'), [c_void_p])
        raster.get_band_description = const_string_output(std_call('GDALGetDescription'), [c_void_p])
        raster.get_band_ds = voidptr_output(std_call('GDALGetBandDataset'), [c_void_p])
        raster.get_band_datatype = int_output(std_call('GDALGetRasterDataType'), [c_void_p])
        raster.get_band_nodata_value = double_output(std_call('GDALGetRasterNoDataValue'), [c_void_p, POINTER(c_int)])
        raster.set_band_nodata_value = void_output(std_call('GDALSetRasterNoDataValue'), [c_void_p, c_double])
        raster.get_band_minimum = double_output(std_call('GDALGetRasterMinimum'), [c_void_p, POINTER(c_int)])
        raster.get_band_maximum = double_output(std_call('GDALGetRasterMaximum'), [c_void_p, POINTER(c_int)])
        
        raster.reproject_image = void_output(std_call('GDALReprojectImage'),[c_void_p, c_char_p, c_void_p, c_char_p, c_int, c_double, c_double, c_void_p, c_void_p, c_void_p])



        
rUpdate = RasterUpdate()


