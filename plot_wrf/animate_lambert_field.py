import netCDF4
from datetime import datetime, timedelta
from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

wrf_out_file = "wrfout_v2_Lambert.nc"

ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')
ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

# NetCDF4-Python can open OPeNDAP dataset just like a local NetCDF file
nc = netCDF4.Dataset(wrf_out_file, 'r')
time_var = nc.variables['Times']
wrfdt = datetime.strptime(''.join(time_var[0]),'%Y-%m-%d_%H:%M:%S')

fig, ax = plt.subplots()

# set up map projection
m = Basemap(llcrnrlon=-95.,llcrnrlat=24.,urcrnrlon=-66.,urcrnrlat=45.)
m.drawcoastlines()
#m.drawparallels(np.arange(0.,180.,30.))
#m.drawmeridians(np.arange(0.,360.,60.))

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are animating three artists, the contour and 2 
# annotatons (title), in each frame
ims = []
for i in range(1, 12):
    im = m.contourf(ds_lon.ReadAsArray()[i], ds_lat.ReadAsArray()[i], ds_t2.ReadAsArray()[i])
    add_arts = im.collections
    text = datetime.strptime(''.join(time_var[i]),'%Y-%m-%d_%H:%M:%S')
    te = ax.text(90, 90, text)
    an = ax.annotate(text, xy=(0.45, 1.05), xycoords='axes fraction')
    ims.append(add_arts + [te,an])

ani = animation.ArtistAnimation(fig, ims)

plt.show()
