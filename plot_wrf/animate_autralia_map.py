from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import netCDF4
from datetime import datetime, timedelta

wrf_out_file = "wrfout_0409.australia.52km.180mins"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')

ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

nc = netCDF4.Dataset(wrf_out_file, 'r')
time_var = nc.variables['Times']

#fig = plt.figure(figsize=(12,8)) 
#ax = fig.add_axes([0.1,0.1,0.8,0.8])
fig, ax = plt.subplots()
plt.title('Temperatures at 2m above the ground in 36 Hours')

map = Basemap(llcrnrlon=110,llcrnrlat=-43,urcrnrlon=151, urcrnrlat=-9,lat_1=45.,lat_2=55,lat_0=-26.,lon_0=130.,resolution='l',projection='gnom')
#projection='gnom', lat_0=-26, lon_0=130, llcrnrlon=108, llcrnrlat=-43, urcrnrlon=152, urcrnrlat=-8, resolution='i', area_thresh=50.0)

map.drawstates(color='0.5')
map.drawcoastlines()
map.drawmapboundary()
#m.fillcontinents()
# draw parallels and meridians.
parallels = np.arange(-60.,90,30.)
map.drawparallels(parallels,labels=[1,0,0,0])
meridians = np.arange(-360.,360.,30.)
map.drawmeridians(meridians,labels=[0,0,0,1])

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are animating three artists, the contour and 2 
# annotatons (title), in each frame
ims = []
for i in range(0, len(ds_t2.ReadAsArray())):
    x, y = map(ds_lon.ReadAsArray()[i], ds_lat.ReadAsArray()[i])
    im = map.contourf(x,y,ds_t2.ReadAsArray()[i])
    add_arts = im.collections
    text = datetime.strptime(''.join(time_var[i]),'%Y-%m-%d_%H:%M:%S')
    te = ax.text(90, 90, text)
    #an = ax.annotate(text, xy=(1.45, 1.05), xycoords='axes fraction')
    ims.append(add_arts + [te])# + [te,an])

ani = animation.ArtistAnimation(fig, ims)
plt.show()
