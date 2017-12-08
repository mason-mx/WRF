load "/usr/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
cdf_file = addfile("/usr/lib/ncarg/data/cdf/contour.cdf","r")
temp = cdf_file->T(0,0,:,:)               ; temperature
lat  = cdf_file->lat                      ; latitude
lon  = cdf_file->lon                      ; longitude
xwks = gsn_open_wks("x11","gsun02n")      ; Open an X11 workstation
plot = gsn_contour(xwks,temp,False)       ; Draw a contour plot.
