from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import netCDF4
from datetime import datetime, timedelta

# Set up formatting for the movie files
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, codec='mpeg4', metadata=dict(artist='Mason'), bitrate=100000)

wrf_out_file = "wrfout_0409.global.27km.6mins-box"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')

ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

nc = netCDF4.Dataset(wrf_out_file, 'r')
time_var = nc.variables['Times']

#fig = plt.figure(figsize=(12,8)) 
#ax = fig.add_axes([0.1,0.1,0.8,0.8])
fig, ax = plt.subplots()
txt = plt.title('Temperatures at 2m above the ground in 36 Hours')

map = Basemap(llcrnrlon=-93.,llcrnrlat=26.,urcrnrlon=-67,urcrnrlat=48.,lat_0=50,lon_0=-106.,resolution='l',projection='merc')

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

#Just plot 240 frames as showing all is at too slow framerate on ARM64
def updatefig(nt):
    global CS1
    x, y = map(ds_lon.ReadAsArray()[nt], ds_lat.ReadAsArray()[nt])
    for c in CS1.collections: c.remove()
    CS1 = map.contourf(x,y,ds_t2.ReadAsArray()[nt],cmap=plt.cm.jet)
    #wrfdt = datetime.strptime(''.join(time_var[nt]),'%Y-%m-%d_%H:%M:%S')
    #txt.set_text(wrfdt)

ani = animation.FuncAnimation(fig, updatefig, interval=100, frames=len(ds_t2.ReadAsArray()))

#ani.save('T2-0404.global.iowrfbox-1080.mp4', writer=writer)

plt.show()
