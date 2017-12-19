load "/usr/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "/usr/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"
load "/usr/lib/ncarg/nclscripts/wrf/WRF_contributed.ncl"

begin
;---Open WRF output file and read data
  dir      = "./"
  filename = "wrfout_v2_Lambert.nc"
  a = addfile(dir + filename,"r")

  times  = wrf_user_list_times(a)  ; get times in the file
  ntimes = dimsizes(times)         ; number of times in the file
  T1 = a->Times
  T1A = wrf_times_c(T1,3)
;  T1A = wrf_times_c(T1(0:0,:),3)
;---Just look at first time step.
  it = 0
  print("Working on time: " + times(it) )

;---Read temperature and terrain height off file
  tc    = wrf_user_getvar(a,"T2",it)     ; T in C
  lat2d = wrf_user_getvar(a,"XLAT",it)   ; latitude
  lon2d = wrf_user_getvar(a,"XLONG",it)  ; longitude
  dims = dimsizes(tc)

;---Start the graphics
  wks = gsn_open_wks("x11","wrf_latlonoverlay")

;---Set some basic plot options
  opts = True
  opts@MainTitle                   = "REAL-TIME WRF"

  pltres = True
  mpres  = True

  opts@TimeLabel = times(it)   ; Set valid time to use on plots

;----------------------------------------------------------------------
; Plot full domain first.
;----------------------------------------------------------------------
  opts@cnFillOn = True  

  contour = wrf_contour(a,wks,tc,opts)
  plot = wrf_map_overlays(a,wks,(/contour/),pltres,mpres)

;----------------------------------------------------------------------
; Plot partial domain.
;----------------------------------------------------------------------
  opts@sfXArray = lon2d
  opts@sfYArray = lat2d

  contour = wrf_contour(a,wks,tc,opts)

;---Set special resource to indicate we are using XLAT/XLONG coordinates.
  pltres@LatLonOverlay = True

;---Zoom in on map, which we can do because we're using lat/lon coordinates.
  mpres@mpLeftCornerLatF  =  30.
  mpres@mpRightCornerLatF =  35.
  mpres@mpLeftCornerLonF  = -85.
  mpres@mpRightCornerLonF = -80.

  plot = wrf_map_overlays(a,wks,(/contour/),pltres,mpres)
end
