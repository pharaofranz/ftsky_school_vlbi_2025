print("Appending the JIVE tables to the IDI FITS files.")
exec(open("add-jive-tables.py").read())

# define a few varibles that hold names of different measurement sets
CONT='ek048d_cont.ms'
GATE='ek048d_gate.ms'
PCAL='pcal.ms'
CHKSRC='chksrc.ms'

print("Loading the data -- gated data go into a separate MS")
importfitsidi(fitsidifile=cont_idifiles, vis=CONT, constobsid=True, scanreindexgap_s=15.0)
importfitsidi(fitsidifile=gate_idifiles, vis=GATE, constobsid=True, scanreindexgap_s=15.0)

print("Writing a summary of the data to disk.")
listobs(vis=CONT, overwrite=True, listfile='listobs_cont.txt')
listobs(vis=GATE, overwrite=True, listfile='listobs_gate.txt')

print("Applying EVN flags, flagging band edges, autocorrelations and other bad data.")
exec(open("flagging.py").read())

print("Applying a-priori calibration using Tsys info from the stations")
exec(open("apriori-cal.py").read())


# if interested we can also correct for ionosperic dispersion
## TEC corrections
#print("Downloading and creating corrections for athmosperic delays (TEC maps).")
#from casatasks.private import tec_maps
#tec_image, tec_rms_image, plotname = tec_maps.create(vis=CONT, doplot=True)
## potentially skip the below (takes 4 mins on 16 cores)
#gencal(vis=CONT, caltable='cont.tecim', caltype='tecim', infile=tec_image)
#
#print("Doing the same for the gated data.")
#tec_image, tec_rms_image, plotname = tec_maps.create(vis=GATE, doplot=True)
#gencal(vis=GATE, caltable='r67.tecim', caltype='tecim', infile=tec_image)

print("Solving for intra-band instrumental delays (single-band-delays).")
# manual fringe fit
fringefit(vis=CONT, caltable='cont.sbd', timerange='15:02:00.0~15:03:00.0', solint='inf', zerorates=True, refant='EF', minsnr=10, gaintable=['cal.gcal', 'cal.tsys'], interp=['nearest','nearest,nearest'], parang=True)

print("Applying SBD corrections to the bandpass calibrator")
# apply single band delay corrections
applycal(vis=CONT, field='J0530+1331', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd'], interp=['nearest','nearest,nearest', 'nearest'], parang=True)

print("Global fringe fitting solving for delays and rates. Applying previous calibration on the fly.")
# global fringe fitting
fringefit(vis=CONT, caltable='cont.mbd', field='J0502+2516, J0530+1331', solint='120s', zerorates=False, refant='EF', minsnr=7, combine='spw', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd'], interp=['nearest','nearest,nearest', 'nearest'], parang=True)

print("Applying fringe fit solutions to the phase calibrator and the fringe finder.")
# apply fringe fit calibration
applycal(vis=CONT, field='J0502+2516, J0530+1331', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd'], interp=['nearest','nearest,nearest', 'nearest', 'linear'], parang=True, spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

print("Creating bandpass corrections from 2 mins of data on the fringe finder.")
# create bandpass calibration
bandpass(vis=CONT, caltable='cont.bpass', field='J0530+1331', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd'], interp=['nearest','nearest,nearest', 'nearest', 'linear'], solnorm=True, solint='inf', refant='EF', bandtype='B', spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], parang=True, minblperant=1)

print("Applying all calibration to the check source.")
# apply calibration to the check source (and phase calibrator)
applycal(vis=CONT, field='J0501+2530', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd', 'cont.bpass'], interp=['nearest','nearest,nearest', 'nearest', 'linear', 'nearest,nearest'], parang=True, spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[]])
#applycal(vis=CONT, field='J0502+2516', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd', 'cont.bpass'], interp=['nearest','nearest,nearest', 'nearest', 'linear', 'nearest,nearest'], parang=True, spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[]])

print("Splitting out the check source for imaging.")
# split out check source (and phase cal)
split(vis=CONT, outputvis='chksrc.ms', field='J0501+2530', correlation='RR, LL', datacolumn='corrected', keepflags=False, width='4', timebin='32s')
#split(vis=CONT, outputvis='pcal.ms', field='J0502+2516', correlation='RR, LL', datacolumn='corrected', keepflags=False, width='4', timebin='32s')

# image phase calibrator, limiting ourselves to the Eff-baselines
#tclean(vis=PCAL, field='J0502+2516', imagename='pcal_scan4.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=128, cell='5mas', weighting='natural', niter=100, interactive=True, savemodel='modelcolumn', restart=True, antenna='5&0; 5&1; 5&2; 5&3; 5&4', scan='4, 38, 78')
print("Imaging the check source to very our calibration is fine.")
# image check source, we restrict ourselves to all Eff-baselines
tclean(vis=CHKSRC, imagename='chksrc.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=128, cell='5mas', weighting='natural', niter=100, interactive=False, savemodel='modelcolumn', restart=False, antenna='5&0; 5&1; 5&2; 5&3; 5&4')

print("Apply the calibration to our gated target scans.")
# apply calibration to target -- make sure to use the correct gcal and tsys
applycal(vis=GATE, field='R67_D', gaintable=['r67.gcal', 'r67.tsys', 'cont.sbd', 'cont.mbd', 'cont.bpass'], interp=['nearest','nearest,nearest', 'nearest', 'linear', 'nearest,nearest'], parang=True, spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[]])

print("Create dirty maps of each burst (scan) separately.")
# get dirty image for all bursts individually, only on Eff baselines
for i in range(1,14):
    tclean(vis=GATE, scan=str(i), imagename='burst'+str(i)+'.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=1024, cell='5mas', weighting='natural', niter=0, savemodel='modelcolumn', restart=False, antenna='5&0; 5&1; 5&2; 5&3; 5&4')

print("Create a dirty map of all bursts (scans) combined ignoring scan 5.")
# get dirty image of combined scans, skip scan 5, only Eff baselines
tclean(vis=GATE, scan='1~4,6~13', imagename='burst_all_but5.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=1024, cell='5mas', weighting='natural', niter=0, savemodel='modelcolumn', restart=False, antenna='5&0; 5&1; 5&2; 5&3; 5&4')
