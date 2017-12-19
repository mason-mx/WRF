# example using matplotlib.animation to create a movie
# reads data over http - needs an active internet connection.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.animation as animation
from osgeo import gdal

wrf_out_file = "wrfout_v2_Lambert.nc"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')

ds_u = gdal.Open('NETCDF:"'+wrf_out_file+'":U10')
ds_v = gdal.Open('NETCDF:"'+wrf_out_file+'":V10')

# make orthographic basemap.
m = Basemap(llcrnrlon=-93.7, llcrnrlat=28., urcrnrlon=-66.1, urcrnrlat=39.5,
              resolution = 'l',
              projection='lcc', lat_1=30., lat_2=60., lat_0=34.83158, lon_0=-98.)

# create figure, add axes (leaving room for colorbar on right)
fig = plt.figure(figsize=(12,8))
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# set desired contour levels.
clevs = np.arange(960,1061,5)
# compute native x,y coordinates of grid.
#x, y = m(ds_lon, ds_lat)
# define parallels and meridians to draw.
parallels = np.arange(-80.,90,20.)
meridians = np.arange(0.,360.,20.)
# number of repeated frames at beginning and end is n1.
nframe = 0; n1 = 10
pos = ax.get_position()
l, b, w, h = pos.bounds

# compute native x,y coordinates of grid.
x, y = m(ds_lon.ReadAsArray()[1], ds_lat.ReadAsArray()[1])

u = ds_u.ReadAsArray()[1]
v = ds_v.ReadAsArray()[1]

yy = np.arange(0, y.shape[0], 4)
xx = np.arange(0, x.shape[1], 4)

# loop over times, make contour plots, draw coastlines, parallels, meridians and title.
CS2 = m.contourf(x, y, np.sqrt(u*u + v*v), alpha = 0.4)
# plot wind vectors over map.
Q = m.quiver(x, y, u, v, scale=500,zorder=10)
# make quiver key.
qk = plt.quiverkey(Q, 0.1, 0.1, 20, '20 m/s', labelpos='W')
# draw coastlines, parallels, meridians, title.
m.drawcoastlines(linewidth=1.5)
#m.drawparallels(parallels)
m.drawmeridians(meridians)
txt = plt.title('SLP and Wind Vectors at 0:00:00 on March 14th, 2017')
# plot colorbar on a separate axes (only for first frame)
cax = plt.axes([l+w-0.05, b, 0.03, h]) # setup colorbar axes
fig.colorbar(CS2,drawedges=True, cax=cax) # draw colorbar
cax.text(0.0,-0.05,'mb')
plt.axes(ax) # reset current axes

def updatefig(nt):
    global CS2,Q
    x, y = m(ds_lon.ReadAsArray()[nt+1], ds_lat.ReadAsArray()[nt+1])

    u = ds_u.ReadAsArray()[nt+1]
    v = ds_v.ReadAsArray()[nt+1]

    for c in CS2.collections: c.remove()
    CS2 = m.contourf(x, y, np.sqrt(u*u + v*v), alpha = 0.4)
    text = 'SLP and Wind Vectors at {0!r}:00:00 on March 14th, 2017'.format(nt+1)
    #urot,vrot,xxx,yyy = m.transform_vector(u, v, xx, yy,51,51,returnxy=True)
    txt.set_text(text)
    Q.set_UVC(u,v)

ani = animation.FuncAnimation(fig, updatefig, frames=11, interval=200)

#ani.save('movie.mp4')

plt.show()
