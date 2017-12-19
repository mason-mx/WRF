from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.animation as animation
import netCDF4
from datetime import datetime, timedelta

wrf_out_file = "/work/wrfout/wrfout_0409.global.27km.2mins"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')
ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

# NetCDF4-Python can open OPeNDAP dataset just like a local NetCDF file
nc = netCDF4.Dataset(wrf_out_file, 'r')
time_var = nc.variables['Times']
wrfdt = datetime.strptime(''.join(time_var[0]),'%Y-%m-%d_%H:%M:%S')

fig = plt.figure(figsize=(30,18)) 
ax = fig.add_axes([0.03,0.03,0.95,0.95])
#([0.01,0.01,0.97,0.97])

# set up Robinson map projection.
m = Basemap(llcrnrlon=-180,llcrnrlat=-80,urcrnrlon=180,urcrnrlat=80,
              projection='mill')
#Basemap(resolution='i',projection='robin',lon_0=0)

CS1 = m.contour(ds_lon.ReadAsArray()[0],ds_lat.ReadAsArray()[0],ds_t2.ReadAsArray()[0],15,linewidths=0.5,colors='k',latlon=True)
CS2 = m.contourf(ds_lon.ReadAsArray()[0],ds_lat.ReadAsArray()[0],ds_t2.ReadAsArray()[0],CS1.levels,cmap=plt.cm.jet,extend='both',latlon=True)

m.colorbar(CS2) # draw colorbar
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawmapboundary()
#m.fillcontinents()
# draw parallels and meridians.
parallels = np.arange(-60.,90,30.)
m.drawparallels(parallels,labels=[1,0,0,0])
meridians = np.arange(-360.,360.,60.)
m.drawmeridians(meridians,labels=[0,0,0,1])
#txt = plt.title('Temperatures at 2m above the ground in 36 Hours')
fig.savefig('foo.png')
#plt.savefig('data.png')

plt.show()
