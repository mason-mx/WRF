from osgeo import gdal
import time

print('================WRF Data Dump==========================');

wrf_out_file = "wrfout_0409.global.27km.6mins-box"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')

ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

while True:
    for i in range(0,len(ds_t2.ReadAsArray())):
        print 'XLONG: ', (ds_lon.ReadAsArray()[i])
        print 'XLAT: ',(ds_lat.ReadAsArray()[i])
        print 'T2: ',(ds_t2.ReadAsArray()[i])
        time.sleep(0.3)

