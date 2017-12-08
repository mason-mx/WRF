import netCDF4
import numpy as np

#Now let's create a new, empty, netCDF file open for writing. Please adjust its name and location for your purposes.
ncfile = netCDF4.Dataset('/tmp/traj.nc','w')

#We will first need to create the 'obs' and 'trajectory' dimensions.
obs_dim = ncfile.createDimension('obs', 5)
trajectory_dim = ncfile.createDimension('trajectory', 2)

#Now we will create some trajectory variables:
#trajectory
#times
#lat
#lon
#z
#geophysical variable(s)
# Defining the 'trajectory' coordinate variable
trajectory = ncfile.createVariable('trajectory', 'i4', ('trajectory',))
trajectory.long_name = ""
trajectory.cf_role = "trajectory_id"

# time
times = ncfile.createVariable('time','f8',('trajectory','obs'))
times.standard_name = 'time'
times.units = 'hours since 2014-06-01T00:00:00Z'
times.axis = 'T'

# lat
lat = ncfile.createVariable('lat', 'f4', ('trajectory','obs'))
lat.units = 'degrees_north'
lat.standard_name = 'latitude'
lat.axis = 'Y'

# lon
lon = ncfile.createVariable('lon', 'f4', ('trajectory','obs'))
lon.units = 'degrees_east'
lon.standard_name = 'longitude'
lon.axis = 'X'

# z
z = ncfile.createVariable('z', 'f4', ('trajectory','obs'))
z.units = 'meter'
z.standard_name = 'altitude'
z.axis = 'Z'
z.positive = "up"

# mean sea level pressure 
mslp = ncfile.createVariable('mslp','f4',('trajectory','obs'))
mslp.units = 'hPa' # hecto-Pascals also known as millibars
mslp.standard_name = 'air_pressure_at_sea_level'
mslp.coordinates = 'time lat lon z'

#Now add the global attributes. If trying to adhere to Unidata Dataset Discovery v1.1, John Caron recommends adding any attribute starting with 'geospatial' or 'time'.
# global attributes
ncfile.Conventions = 'CF-1.6'
ncfile.Metadata_Conventions = 'Unidata Dataset Discovery v1.0'
ncfile.featureType = 'trajectory'
ncfile.cdm_data_type = 'Trajectory'
ncfile.nodc_template_version = 'NODC_NetCDF_Trajectory_Template_v0.9'
ncfile. standard_name_vocabulary = 'CF-1.6'

#Finally, let us add the actual (in this case fake) data.
# trajectory IDs
trajectory[:] = np.array([17,42])

# times (hours since 2014-06-01T00:00:00Z)
times[:] = np.array([[0, 0, 0, 0, 0], [12, 12, 12, 12, 12]])

# lat/lon/z
lat[:] = np.array([[40, 40, 40, 40, 40], [41, 41, 41, 41, 41]])
lon[:] = np.array([[-106, -106, -106, -106, -106], [-107, -107, -107, -107, -107]])
z[:] = np.array([[0, 1000, 2000, 3000, 4000], [0, 1000, 2000, 3000, 4000]])

# mean sea level pressure
mslp[:] = np.array([[1000, 950, 800, 700, 625], [990, 940, 810, 690, 620]])

# Close the netCDF file
ncfile.close()
