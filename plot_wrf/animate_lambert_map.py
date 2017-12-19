from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import netCDF4
from datetime import datetime, timedelta

wrf_out_file = "wrfout_0409.lambert.30km.60mins"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')

ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

nc = netCDF4.Dataset(wrf_out_file, 'r')
time_var = nc.variables['Times']

#fig = plt.figure(figsize=(12,8)) 
#ax = fig.add_axes([0.1,0.1,0.8,0.8])
fig, ax = plt.subplots()
txt = plt.title('Temperatures at 2m above the ground in 36 Hours')

map = Basemap(llcrnrlon=-95.,llcrnrlat=27.,urcrnrlon=-65,urcrnrlat=40.,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.,resolution='l',projection='tmerc')

map.drawstates(color='0.5')
map.drawcoastlines()
map.drawmapboundary()
#m.fillcontinents()

x, y = map(ds_lon.ReadAsArray()[0], ds_lat.ReadAsArray()[0])
CS1 = map.contour(x,y,ds_t2.ReadAsArray()[0])

# draw parallels and meridians.
parallels = np.arange(-60.,90,30.)
map.drawparallels(parallels,labels=[1,0,0,0])
meridians = np.arange(-360.,360.,30.)
map.drawmeridians(meridians,labels=[0,0,0,1])

def updatefig(nt):
    global CS1
    x, y = map(ds_lon.ReadAsArray()[nt], ds_lat.ReadAsArray()[nt])
    for c in CS1.collections: c.remove()
    print (ds_lon.ReadAsArray()[nt])
    print (ds_lat.ReadAsArray()[nt])
    print (ds_t2.ReadAsArray()[nt])
    CS1 = map.contourf(x,y,ds_t2.ReadAsArray()[nt])
    wrfdt = datetime.strptime(''.join(time_var[nt]),'%Y-%m-%d_%H:%M:%S')
    txt.set_text(wrfdt)

ani = animation.FuncAnimation(fig, updatefig, frames=len(ds_t2.ReadAsArray()))

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are animating three artists, the contour and 2 
# annotatons (title), in each frame
#ims = []
#for i in range(0, len(ds_t2.ReadAsArray())):
#    x, y = map(ds_lon.ReadAsArray()[i], ds_lat.ReadAsArray()[i])
#    im = map.contourf(x,y,ds_t2.ReadAsArray()[i])
#    add_arts = im.collections
#    text = datetime.strptime(''.join(time_var[i]),'%Y-%m-%d_%H:%M:%S')
#    te = ax.text(90, 90, text)
#    #an = ax.annotate(text, xy=(1.45, 1.05), xycoords='axes fraction')
#    ims.append(add_arts + [te])# + [te,an])
#
#ani = animation.ArtistAnimation(fig, ims)
plt.show()
