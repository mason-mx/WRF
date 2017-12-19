;----------------------------------------------------------------------
; wrf_gsn_4.ncl
;----------------------------------------------------------------------
; Concepts illustrated:
;   - Using gsn_csm scripts to plot WRF-ARW data
;   - Setting the correct WRF map projection using wrf_map_resources
;----------------------------------------------------------------------
; This script is meant to show the difference between plotting WRF
; data using wrf_xxx scripts, and using gsn_csm_xxx scripts.
;
; See wrf_nogsn_4.ncl for an example of using wrf_xxxx scripts to
; plot WRF data.
;----------------------------------------------------------------------
; In NCL Versions 6.3.1 and earlier, you will get these warnings which
; you can safely ignore:
;
; warning:start_lat is not a valid resource in wrf_gsn_contour at this time
; warning:start_lon is not a valid resource in wrf_gsn_contour at this time
; warning:end_lat is not a valid resource in wrf_gsn_contour at this time
; warning:end_lon is not a valid resource in wrf_gsn_contour at this time
; warning:mpNestTime is not a valid resource in map at this time
;----------------------------------------------------------------------
; These files are loaded by default in NCL V6.2.0 and newer
; load "/usr/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "/usr/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "/usr/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

begin
;---Open WRF output file
  filename = "wrfout_d02_2017-04-09_australia"
  a        = addfile(filename,"r")

;---Read temperature at first time step
  tc = wrf_user_getvar(a,"tc",0)

  wks = gsn_open_wks("png","wrf_gsn")

;---Resources for filled contour plot
  res                      = True

  res@gsnMaximize          = True

  res@cnFillOn             = True  
  res@cnLinesOn            = False
  res@cnLevelSpacingF      = 2.           ; NCL chose 4.0
  res@lbOrientation        = "Vertical"
  res@tiMainString         = filename 

;---Necessary for contours to be overlaid correctly on WRF projection
  res@tfDoNDCOverlay       = True
  res@gsnAddCyclic         = False

;---Set map resources based on projection on WRF output file
  res = wrf_map_resources(a,res)

;---Call plotting routine which draws contours over a map
  nl   = 0    ; bottomost level
  plot = gsn_csm_contour_map(wks,tc(nl,:,:),res)
end

