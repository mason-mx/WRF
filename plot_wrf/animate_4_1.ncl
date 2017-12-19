;======================================================================
; animate_4_1.ncl
;
; Concepts illustrated:
;   - Creating animations
;   - Animating WRF reflectivity data over a terrain map across time and levels
;   - Using get_cpu_time to calculate the CPU time for a script to execute
;   - Drawing partially transparent filled contours
;   - Drawing raster and smooth contours
;   - Using two different colormaps on one frame
;   - Paneling four plots on a page.
;   - Using functions for cleaner code
;   - Adding a common labelbar to paneled plots
;   - Adding figure strings to paneled plots
;======================================================================
; This example generates an animation aross time and four given levels
; of filled contours of reflectivity overlaid on a terrain map. The 
; reflectivity field changes with each time step and level, while the
; terrain  map is static.
;
; This example shows the more "traditional" way of generating both sets
; of contours, by calling "gsn_csm_contour", "gsn_csm_contour_map" and
; "overlay" inside a "do" loop. This method can be slow if you have a 
; lot of time steps, or if you are needlessly regenerating the same plot 
; over and over (like the terrain map). 
;
; See animate_4_2.ncl for a faster method of generating these plots.
;======================================================================
; See animate_3_1.ncl for the more traditional method of generating the
; same set of plots, and animate_3_2.ncl for another faster method.
;======================================================================

;======================================================================
; This function creates and draws a labelbar based on a given 
; contour plot.
;======================================================================
function labelbar(wks,plot)
local colors, levels, labels, nboxes, bb, bot
begin
;---Get bounding box that encloses plot, so we know where the bottom edge is.
  bb  = NhlGetBB(plot)
  bot = bb(1)             ; bottom edge of plot

;---Retrieve the contour levels and their associated colors.
  getvalues plot
    "cnLevels"     : levels
    "cnFillColors" : colors
  end getvalues

  nboxes = dimsizes(colors)

  labels                   = ""+levels    ; labels for the labelbar

;---Set some labelbar resources.
  lbres                    = True
  lbres@vpXF               = 0.15         ; Position labelbar at         
  lbres@vpYF               = 0.10
  lbres@vpWidthF           = 0.70
  lbres@vpHeightF          = 0.10

  lbres@lbPerimOn          = False            ; Turn off perimeter.
  lbres@lbOrientation      = "Horizontal"     ; Default is vertical.
  lbres@lbFillColors       = colors
  lbres@lbMonoFillPattern  = True             ; Fill them all solid.
  lbres@lbLabelFontHeightF = 0.013            ; Label font height
  lbres@lbLabelAlignment   = "InteriorEdges"

  lbid = gsn_create_labelbar(wks,nboxes,labels,lbres)

  draw(lbid)     ; Draw labelbar

  return(lbid)   ; Return it so we can maximize later if desired.
end

;----------------------------------------------------------------------
; Main code
;----------------------------------------------------------------------
begin
  start_cpu_time = get_cpu_time()     ; We will time this example

;---Open files
  dir   = "./"
  files = systemfunc("ls " + dir + "wrfout_v2_*")
  a     = addfiles(files,"r")

;---Read variables
  hgt   = a[:]->HGT(0,:,:)                 ; terrain, 0 is the first time step
  znu   = a[:]->ZNU                        ; (Time, bottom_top)
  dbz   = wrf_user_getvar(a,"dbz",-1)      ; reflectivity  [Time | 97] x [bottom_top | 32] x 
                                           ;       [south_north | 197] x [west_east | 206]
  times = wrf_user_list_times(a)           ; time as character strings

  printMinMax(dbz,0)
  printVarSummary(dbz)

;---Set all values < -28 to missing, so they don't get contoured.
  dbz@_FillValue = -999.
  dbz            = where(dbz.lt.-28,dbz@_FillValue,dbz)
  ntim           = dimsizes(dbz(:,0,0,0))
  ilevels        = (/5,15,20,25/)           ; which level indexes to plot; levels 26
                                            ; and higher tend to have missing data
  nlev           = dimsizes(ilevels)
  ter_plot       = new(nlev,graphic)
  dbz_plot       = new(nlev,graphic)

;---Open workstation
  wks = gsn_open_wks("png","animate")

;---Set some common resources
  res                       = True
  res@gsnDraw               = False    ; turn off draw
  res@gsnFrame              = False    ; turn off frame
  res@cnFillOn              = True     ; turn on contour fill
  res@cnLinesOn             = False    ; turn off contour lines
  res@cnLineLabelsOn        = False    ; turn off contour line labels
  res@cnInfoLabelOn         = False    ; turn off info label

  res@gsnLeftString         = ""       ; turn off subtitles
  res@gsnRightString        = ""
  res@gsnCenterString       = ""

  res@lbLabelFontHeightF       = 0.015    ; size of labelbar labels
  res@pmLabelBarOrthogonalPosF = -0.02    ; move labelbar closer to plot
  res@tfDoNDCOverlay           = True     ; faster plotting if we use 
                                          ; native WRF map projection
  res@lbLabelBarOn             = False    ; will add to panel plot

;---Copy common resources for terrain plot
  tres = res 
  tres = wrf_map_resources(a[0],tres)    ; Use first file in list for map proj info

  tres@cnLevelSelectionMode  = "ExplicitLevels"
  tres@cnLevels              = ispan(1,2200,200)
  tres@cnFillPalette         = "OceanLakeLandSnow"
  tres@cnFillOpacityF        = 0.5                 ; make contours partially transparent

;---Copy common resources for dbz plot
  dres                       = res      

  dres@cnFillMode            = "RasterFill"
  dres@cnLevelSelectionMode  = "ExplicitLevels"
  dres@cnLevels              = ispan(-28,50,8)

;---Read in colormap so we can subset it.
  cmap_r                     = read_colormap_file("WhViBlGrYeOrRe")
  dres@cnFillPalette         = cmap_r(6:,:)  ; skip the first few colors

;---Panel resources
  pres                  = True
  pres@gsnFrame         = False   ; so we can add a labelbar 
  pres@gsnPanelBottom   = 0.1
;
; Loop through each time step and draw a set of paneled plots
; Time 0 has constant fields, so skip it.
;
  do nt=1,ntim-1

;---For each set of levels, check for all missing or constant fields
    skip_this_one = False
    first         = True
    do nl=0,nlev-1
      ilev  = ilevels(nl)
      if(all(ismissing(dbz(nt,ilev,:,:))).or.(min(dbz(nt,ilev,:,:)).eq.max(dbz(nt,ilev,:,:)))) then
        print("Field is constant at time='" + times(nt) + "' and level=" + znu(nt,ilev) +". Skipping...")
        skip_this_one = True
        continue
      else
        print("time  ='" + times(nt) + "'")
        print("level =" + znu(nt,ilev))
      end if
    end do

;---Skip this time step if one or more plots would be invalid.
    if(skip_this_one) then
      continue
    end if

;---For each set of levels, generate a 2 x 2 panel plot
    do nl=0,nlev-1
      ilev  = ilevels(nl)
      ter_plot(nl) = gsn_csm_contour_map(wks,hgt,tres)
      dbz_plot(nl) = gsn_csm_contour(wks,dbz(nt,ilev,:,:),dres)

;---Create a labelbar just once
      if(first) then
        lbid = labelbar(wks,dbz_plot(nl))
        first = False
      end if
      overlay(ter_plot(nl),dbz_plot(nl))
    end do

;---Draw the labelbar at the bottom and then the four paneled plots
    draw(lbid)
    pres@gsnPanelFigureStrings = ""+znu(nt,ilevels)
    pres@txString              = times(nt)
;;  pres@gsnPanelMainString    = times(nt)     ; V6.4.0 or later
    gsn_panel(wks,ter_plot,(/2,2/),pres)
    frame(wks)                           ; Advance the frame
  end do

;---Calculate total time for this example.
  end_cpu_time = get_cpu_time()
  print(get_script_prefix_name() + ": elapsed time = " + (end_cpu_time-start_cpu_time) + " seconds.")
end
