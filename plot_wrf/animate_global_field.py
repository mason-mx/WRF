from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.animation as animation
import netCDF4
from datetime import datetime, timedelta

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, codec='mpeg4', metadata=dict(artist='Mason'), bitrate=100000)

wrf_out_file = "wrfout_0409.global.27km.6mins"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')
ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

# NetCDF4-Python can open OPeNDAP dataset just like a local NetCDF file
nc = netCDF4.Dataset(wrf_out_file, 'r')
time_var = nc.variables['Times']
wrfdt = datetime.strptime(''.join(time_var[0]),'%Y-%m-%d_%H:%M:%S')

fig = plt.figure(figsize=(24,16)) 
ax = fig.add_axes([0.01,0.01,0.97,0.97])#([0.1,0.1,0.8,0.8])

# set up Robinson map projection.
m = Basemap(resolution='i',projection='robin',lon_0=0)

#m.colorbar(CS2) # draw colorbar
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawmapboundary()
#m.fillcontinents()
# draw parallels and meridians.
parallels = np.arange(-60.,90,30.)
m.drawparallels(parallels,labels=[1,0,0,0])
meridians = np.arange(-360.,360.,60.)
m.drawmeridians(meridians,labels=[0,0,0,1])
txt = plt.title('')

#Followed code works just on x86, not ARM64
#def updatefig(nt):
#    global CS2, CS1
#    for c in CS1.collections: c.remove()
#    CS1 = m.contour(ds_lon.ReadAsArray()[nt],ds_lat.ReadAsArray()[nt],ds_t2.ReadAsArray()[nt],15,linewidths=0.5,colors='k',latlon=True)
#    for c in CS2.collections: c.remove()    
#    CS2 = m.contourf(ds_lon.ReadAsArray()[nt],ds_lat.ReadAsArray()[nt],ds_t2.ReadAsArray()[nt],CS1.levels,cmap=plt.cm.jet,extend='both',latlon=True)
#    wrfdt = datetime.strptime(''.join(time_var[nt]),'%Y-%m-%d_%H:%M:%S')
#    txt.set_text(wrfdt)

#ani = animation.FuncAnimation(fig, updatefig, frames=len(ds_t2.ReadAsArray()))

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are animating three artists, the contour and 2 
# annotatons (title), in each frame
ims = []
for i in range(0, len(ds_t2.ReadAsArray())):
    im = m.contour(ds_lon.ReadAsArray()[i],ds_lat.ReadAsArray()[i],ds_t2.ReadAsArray()[i],15,linewidths=0.5,colors='k',latlon=True)
    im2 = m.contourf(ds_lon.ReadAsArray()[i],ds_lat.ReadAsArray()[i],ds_t2.ReadAsArray()[i],im.levels,cmap=plt.cm.jet,extend='both',latlon=True)

    add_arts = im.collections
    #text = datetime.strptime(''.join(time_var[i]),'%Y-%m-%d_%H:%M:%S')
    #te = ax.text(90, 90, text)
    #an = ax.annotate(text, xy=(0.45, 1.05), xycoords='axes fraction')
    ims.append(add_arts + im2.collections)# + [an])
    #ims.append(add_arts + im2.collections + [te,an])

ani = animation.ArtistAnimation(fig, ims)

ani.save('T2-global-1080.mp4', writer=writer)

plt.show()
