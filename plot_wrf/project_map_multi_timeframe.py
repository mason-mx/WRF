import netCDF4
from datetime import datetime, timedelta
from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys

wrf_out_file = "wrfout_0409.global.27km.2mins-box"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')
ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

nc = netCDF4.Dataset(wrf_out_file, 'r')
time_var = nc.variables['Times']

frame = 0
# create new figure
fig=plt.figure()
text = datetime.strptime(''.join(time_var[frame]),'%Y-%m-%d_%H:%M:%S')
print(text);
map = Basemap(llcrnrlon=-95.,llcrnrlat=27.,urcrnrlon=-65.,urcrnrlat=40.,
              projection='lcc', lat_1=30.,lat_2=60.,lat_0=34.83158,lon_0=-98.)

x, y = map(ds_lon.ReadAsArray()[frame], ds_lat.ReadAsArray()[frame])

map.contourf(x, y, ds_t2.ReadAsArray()[frame]) 

map.drawcoastlines()
plt.title(text)

frame = 18
# create new figure
fig=plt.figure()
text = datetime.strptime(''.join(time_var[frame]),'%Y-%m-%d_%H:%M:%S')
print(text);
map = Basemap(llcrnrlon=-95.,llcrnrlat=27.,urcrnrlon=-65.,urcrnrlat=40.,
              projection='lcc', lat_1=30.,lat_2=60.,lat_0=34.83158,lon_0=-98.)

x, y = map(ds_lon.ReadAsArray()[frame], ds_lat.ReadAsArray()[frame])

map.contourf(x, y, ds_t2.ReadAsArray()[frame]) 

map.drawcoastlines()
plt.title(text)

frame = 36
# create new figure
fig=plt.figure()
text = datetime.strptime(''.join(time_var[frame]),'%Y-%m-%d_%H:%M:%S')
print(text);
map = Basemap(llcrnrlon=-95.,llcrnrlat=27.,urcrnrlon=-65.,urcrnrlat=40.,
              projection='lcc', lat_1=30.,lat_2=60.,lat_0=34.83158,lon_0=-98.)

x, y = map(ds_lon.ReadAsArray()[frame], ds_lat.ReadAsArray()[frame])

map.contourf(x, y, ds_t2.ReadAsArray()[frame]) 

map.drawcoastlines()
plt.title(text)

plt.show()
