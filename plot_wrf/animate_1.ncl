;*************************************************
; animate_1.ncl           
;************************************************
;
; Concepts illustrated:
;   - Creating animations
;   - Changing the data in a contour/map plot using "setvalues"
;   - Creating a color map using RGB triplets
;   - Turning off the addition of a longitude cyclic point
;   - Turning off the subtitles at the top of a plot
;   - Turning off the box lines in a labelbar
;   - Setting a nice stride for labelbar labels
;

load "/usr/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "/usr/lib/ncarg/nclscripts/csm/gsn_csm.ncl"

begin
;
; Open a netCDF file and read some data.
;
  dir = ncargpath("data") + "/cdf/"
  a   = addfile(dir + "meccatemp.cdf","r")
  t   = a->t(0,:,:)                     ; Read first time step

; Define a color map using RGB triplets
  cmap = (/(/1.00,1.00,1.00/),(/.000,.000,.000/),(/.700,.700,.700/), \
           (/.650,.650,.700/),(/.610,.600,.700/),(/.550,.550,.700/), \
           (/.560,.500,.700/),(/.450,.450,.700/),(/.420,.400,.700/), \
           (/.350,.350,.700/),(/.300,.300,.700/),(/.250,.250,.700/), \
           (/.200,.200,.700/),(/.150,.150,.700/),(/.100,.100,.700/), \
           (/.050,.050,.700/),(/.000,.000,.700/),(/.000,.050,.700/), \
           (/.000,.100,.700/),(/.000,.150,.700/),(/.000,.200,.700/), \
           (/.000,.250,.700/),(/.000,.300,.700/),(/.000,.350,.700/), \
           (/.000,.400,.700/),(/.000,.450,.600/),(/.000,.500,.500/), \
           (/.000,.550,.400/),(/.000,.600,.300/),(/.000,.650,.200/), \
           (/.000,.700,.100/),(/.000,.725,.000/),(/.000,.690,.000/), \
           (/.030,.685,.000/),(/.060,.680,.000/),(/.100,.575,.000/), \
           (/.130,.570,.000/),(/.160,.565,.000/),(/.550,.550,.000/), \
           (/.555,.545,.000/),(/.560,.530,.000/),(/.565,.485,.000/), \
           (/.570,.420,.000/),(/.675,.375,.000/),(/.680,.330,.000/), \
           (/.690,.300,.000/),(/.700,.285,.000/),(/.700,.270,.000/), \
           (/.700,.260,.000/),(/.700,.240,.000/),(/.700,.180,.000/), \
           (/.700,.130,.000/),(/.700,.120,.000/),(/.700,.100,.000/), \
           (/.700,.090,.000/),(/.750,.090,.000/),(/.800,.090,.000/), \
           (/.830,.070,.000/),(/.870,.050,.000/),(/.900,.030,.000/), \
           (/.950,.010,.000/),(/.990,.000,.000/),(/1.00,.000,.000/), \
           (/1.00,.000,.000/)/)

;
; Start the graphics.
;
; The gsn_open_wks call will create a file called "animate.ncgm".
; You can use the tool "idt" (which comes with NCL) to animate it.
;
; First type:
;
;   idt animate.ncgm
;
; Three panels should pop up. One of them has an "animate" button.
; Click on this, and each frame will be loaded into memory.
; When this is done, click ">>" or "<<" to play the animation.
; Use "delay" to slow down the animation, or "loop" to repeat it.
;
; See: http://www.ncl.ucar.edu/Document/Tools/idt.shtml
;
  wks = gsn_open_wks("ps","animate")
  gsn_define_colormap(wks,cmap)

  res                      = True

  res@gsnMaximize          = True  
  res@gsnAddCyclic         = False   ; Don't add longitude cyclic pt.

  res@gsnLeftString        = ""      ;  Make sure no subtitles
  res@gsnRightString       = ""

  res@cnFillOn             = True    ; Turn on contour fill.

  res@cnLevelSelectionMode = "ManualLevels"
  res@cnMinLevelValF       =  195.0
  res@cnMaxLevelValF       =  328.0
  res@cnLevelSpacingF      = 2.25

  res@cnLinesOn            = False   ; Turn off the contour lines.
  res@cnLineLabelsOn       = False   ; Turn off the contour line labels.

  res@lbLabelAutoStride    = True    ; Nice spacing for labelbar labels.
  res@lbBoxLinesOn         = False   ; Turn off labelbar box lines

  res@mpFillOn             = False   ; Turn off map fill.
  res@mpCenterLonF         = 150.0

  res@tiMainString         = "January Global Surface Temperature (K) - Day 1"

  plot = gsn_csm_contour_map(wks,t,res)

  ntimes = dimsizes(a->t(:,0,0))
  do i=1,ntimes-1
;
; The more efficient way to do animations is to use "setvalues"
; to change the data only.
;
; Use "(/.../)" to avoid re-reading the coordinate arrays, which are
; the same for every timestep.
;
    setvalues plot@data
      "sfDataArray" : (/a->t(i,:,:)/)
    end setvalues

; Use setvalues to change the title too.
    setvalues plot
      "tiMainString"  : "January Global Surface Temperature - Day " + (i+1)
    end setvalues
  
; Draw the plot and advance the frame.
;    draw(plot)
;    frame(wks)
    maximize_output(wks,False)
;
; You can accomplish the same thing by removing all the code above
; from the "do" call, and just use the below two lines. The code will run
; slower, however, because it will regenerate the contour-map every 
; single time, and it has to read in the data and the coordinate arrays
; in every iteration.
;
;    res@tiMainString =  "January Global Surface Temperature - Day " + (i+1)
;    plot = gsn_csm_contour_map(wks,a->t(i,:,:),res)
  end do

end
