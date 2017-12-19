; load functions and procedures
load "/usr/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "/usr/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"
load "/usr/lib/ncarg/nclscripts/wrf/WRF_contributed.ncl"

begin
 
; WRF ARW input file (NOTE, your wrfout file does not need 
; the .nc, but NCL needs it so make sure to add it in the 
; line below)
a = addfile("./wrfout_v2_Lambert.nc","r") 

 
; Output on screen. Output will be called "plt_Surface1"
type = "x11"
wks = gsn_open_wks(type,"plt_Surface1") 

 
; Set basic resources
res = True
res@MainTitle = "REAL-TIME WRF"          ; Give plot a main title
res@Footer = False                              ; Set Footers off
pltres = True                                ; Plotting resources 
mpres = True                                      ; Map resources
 
;---------------------------------------------------------------
times = wrf_user_getvar(a,"Times",0)    ; get times in the file
it = 0                            ; only interested in first time
res@TimeLabel = times(it)            ; keep some time information
Time  = WRF_times_c(times, 0)   
;---------------------------------------------------------------
; Get variables
 
t2 = wrf_user_getvar(a,"T2",it)                  ; Get T2 (deg K)
   tc2 = t2-273.16                             ; Convert to deg C
   tf2 = 1.8*tc2+32.                           ; Convert to deg F
   tf2@description = "Surface Temperature"
   tf2@units = "F"
 
u10 = wrf_user_getvar(a,"U10",it)                       ; Get U10
v10 = wrf_user_getvar(a,"V10",it)                       ; Get V10
   u10 = u10*1.94386                           ; Convert to knots
   v10 = v10*1.94386
   u10@units = "kts"
   v10@units = "kts"
 
;---------------------------------------------------------------



; Plotting options for T
opts = res                                  ; Add basic resources
opts@cnFillOn = True                                ; Shaded plot
opts@ContourParameters = (/ -20., 90., 5./)   ; Contour intervals
opts@gsnSpreadColorEnd = -3
contour_tc = wrf_contour(a,wks,tf2,opts)            ; Create plot
delete(opts)
 
 
; Plotting options for Wind Vectors
opts = res                                  ; Add basic resources
opts@FieldTitle = "Winds"             ; Overwrite the field title
opts@NumVectors = 47                      ; Density of wind barbs
vector = wrf_vector(a,wks,u10,v10,opts)             ; Create plot
delete(opts)
 
 
; MAKE PLOTS 
plot = wrf_map_overlays(a,wks,contour_tc,pltres,mpres)
 
;---------------------------------------------------------------
 
 
end
