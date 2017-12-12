# WRF

1. Post-Processing Utilities and Tools
a. NCL based scripts
NCL is a free interpreted language designed for scientific data processing and visualization.  NCL Is available for a variety of operating systems including Linux, Mac OS X, and Cygwin/X running on Windows. It supports netCDF 3/4, GRIB 1/2, HDF 4/5, HDF_EOS 2/5, shapefile, ASCII, binary. Refer to http://www.ncl.ucar.edu/.
NCL based code on http://www2.mmm.ucar.edu/wrf/OnLineTutorial/Graphics/NCL/NCL_examples.htm

plotgrids.ncl
It is a script to read the WPS namelist and plot corresponding domains. Refer to http://www2.mmm.ucar.edu/wrf/OnLineTutorial/Graphics/NCL/Examples/EXPERIMENTAL/wrf_show_wps_som_namelist.htm

wrfout_to_cf.ncl
It is an NCL based script to create new CF based NetCDF files from native wrfout NetCDF files. Refer to http://foehn.colorado.edu/wrfout_to_cf/.

------------------------------------------------------
To get started with NCL
ncl_tutorial_1.ncl
Refer to https://code.mpimet.mpg.de/projects/miklip-d-integration/wiki/NCL_simple_plot#NCL.

b. WRF Utilities Downloads (fortran code) on http://www2.mmm.ucar.edu/wrf/users/download/get_sources.html#utilities

read_wrf_nc
– Display data in a wrfout netCDF file
– Specific points; min/max of fields; time series; edit data in file (NCL better)
Compile 
Refer to the following troubleshooting as extra code should be included.
Run
./read_wrf_nc  wrf_data_file_name  [-options]
Refer to http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_V3.9/users_guide_chap10.htm#read_wrf_nc.

iowrf
– Thinning ofnetCDF data; extracting a area; destaggering grid
Compile 
Refer to the following troubleshooting as extra code should be included.
Run
./iowrf  wrf_data_file_name  [-options]
Refer to http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_V3.9/users_guide_chap10.htm#iowrf.

wrf_interp
gfortran -o wrf_interp.exe wrf_interp.F90 -I/home/mason/build_wrf/LIBRARIES/netcdff/include -free -L/home/mason/build_wrf/LIBRARIES/netcdf/lib -lnetcdff -lnetcdf

------------------------------------------------------
Toubleshooting
If you meet the problem: iowrf.f:(.text+0x7b6): undefined reference to `iargc_'
collect2: error: ld returned 1 exit status
Do as below:
Compiling read_wrf_nc/iowrf with gfortran
gfortran lacks iargc, so compile gfortran_iargc.c at first
$ gfortran -c gfortran_iargs.c
then
$ gfortran gfortran_iargc.o read_wrf_nc.f90 -L$NETCDF/lib -lnetcdf -I/$NETCDF/include -ffree-form -o read_wrf_nc/iowrf 
in my case $ gfortran gfortran_iargc.o iowrf.f -L/home/mason/build_wrf/LIBRARIES/netcdf/lib -I/home/mason/build_wrf/LIBRARIES/netcdff/include -lnetcdff -lnetcdf -lm -ffree-form -o read_wrf_nc/iowrf


