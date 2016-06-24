# This code creates a raster from a shapefile.
# Every feature in the shapefile is included in the raster.

import os
import gdal
import ogr    
import sys

os.chdir(r'C:\Users\pipi\Documents\Rogaine\Tarlo\gpx')  #folder containing gpx files
vector_fn = 'gpxcollection.shp'  #filename of input shapefile
pixel_size = 15 #same unit as coordinates
raster_fn = 'test.tif'  # Filename of the raster Tiff that will be created

driver = ogr.GetDriverByName('ESRI Shapefile')

#______Open's the data source and reads the extent________

try:
    source_ds = driver.Open(vector_fn, 0) #0 means read only# Check to see if shapefile is found.

    if source_ds is None:
        print 'Could not open %s' % (vector_fn)
        sys.exit()
        
    else:
        try:
            source_layer = source_ds.GetLayer()  #returns the first layer in the data source
            x_min, x_max, y_min, y_max = source_layer.GetExtent()

            # determines the x and y resolution of the raster file
            x_res = int((x_max - x_min) / pixel_size)
            y_res = int((y_max - y_min) / pixel_size)

            #______Create the destination raster file__________
            try:
                # create the target raster file with 1 band
                target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)
                target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
                target_ds.SetProjection(source_layer.GetSpatialRef().ExportToWkt())
                band = target_ds.GetRasterBand(1)

                #______Populates the raster file with the data from the shapefile____
                gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[1])

            finally:
                target_ds = None  #flushes data from memory.  Without this you often get an empty raster.

        finally:
            source_layer = None

finally:
    source_ds = None
