<!-- MathJax -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script> 
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({
      tex2jax: {
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
        inlineMath: [['$','$']],
        displayMath: [['$$','$$']]
      }
    });
</script> 

<script type="text/javascript">
var pcs = document.lastModified.split(" ")[0].split("/");
var date = pcs[1] + '/' + pcs[0] + '/' + pcs[2];
onload = function(){
    document.getElementById("lastModified").innerHTML = "Page last modified on " + date;
}
		</script>

<link href="styles.css" rel="stylesheet" />

<!-- Prism CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" />
<link id="prism-dark" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" disabled />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css" />

<!-- Prism JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>

# FTSky VLBI workshop 2025

Welcome! This page hosts the **tutorial materials** and **guides** from the **FTSky
Workshop**, held at **ICTS Bengaluru** on **06–10 October 2025**.

# VLBI tutorial
## Download the data

```bash
wget -t45 -l1 -r -nd https://archive.jive.eu/exp/EK048D_210410/fits -A "ek048d*"
wget https://archive.jive.nl/exp/EK048D_210410/pipe/ek048d.uvflg
wget https://archive.jive.nl/exp/EK048D_210410/pipe/ek048d.antab.gz
```

## How to handle the containers
### Apptainer
- install apptainer following the [installation instructions](https://apptainer.org/docs/admin/main/installation.html)
- download the image

```bash
wget https://franzkirsten.de/ftsky.simg
```

- start up the image to work "interactively"

```bash
singularity shell -e --env DISPLAY=$DISPLAY --fakeroot -B /path/to/data:/data ftsky.simg
```

- test if things are working correctly:
  - If you see errors about `fuse` and `fusermount` you may have forgotten to add
    `--fakeroot`
  - Try to start up `casaviewer` (just type it at the prompt and hit `return`). If you get
    two windows where you can open files and no errors are printed to the prompt you're
    all good to go.
  - In case you get errors about x-forwarding not working, you may have forgotten to add
    `--env DISPLAY=$DISPLAY`
  - In case windows do pop up but they're just gray and there are loads of error messages
    on the prompt, you may need to `exit` from the container and run `xhost +local:root;
    xhost +local:apptainer`; and then start the container again.

### Docker
- install docker following the [installation instructions](https://docs.docker.com/engine/install/)
- pull the image from docker

```bash
docker pull apal52/radio-img
```

- prepare your environment to allow X-forwarding from the docker container

```bash
xhost +local:docker
# may also need
xhost +local:root
```

- spin up the container to run things "interactively"

```bash
docker run -it --privileged -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix --ipc=host -v $(pwd):/data <container-name>
```

- test if things are working correctly:
  - If you see errors about `fuse` and `fusermount` you may have forgotten to add
    `--privileged`
  - Try to start up `casaviewer` (just type it at the prompt and hit `return`). If you get
    two windows where you can open files and no errors are printed to the prompt you're
    all good to go.
  - In case you get errors about x-forwarding not working, you may have forgotten to add
    `-e DISPLAY=$DISPLAY`

## Tutorial

### Preliminary steps
- to get JIVE pipeline tables into casa
```python
from casavlbitools import fitsidi
myidifiles = sorted(glob.glob('ek048d*IDI*'))
fitsidi.append_tsys('ek048d.antab',myidifiles)
fitsidi.append_gc('ek048d.antab',myidifiles[0])
fitsidi.convert_flags('ek048d.uvflg', myidifiles, outfile='ek048d.flag')
```
### Basic steps
- Load the data into casa

```python
# define a few varibles that hold names of different measurement sets
CONT='ek048d_cont.ms'
GATE='ek048d_gate.ms'
PCAL='pcal.ms'
CHKSRC='chksrc.ms'

importfitsidi(fitsidifile=['ek048d_1_1.IDI1', 'ek048d_1_1.IDI2', 'ek048d_1_1.IDI3','ek048d_1_1.IDI4', 'ek048d_1_1.IDI5', 'ek048d_1_1.IDI6'],vis=CONT, constobsid=True, scanreindexgap_s=15.0)
importfitsidi(fitsidifile=['ek048d_2_1.IDI'],vis=GATE, constobsid=True, scanreindexgap_s=15.0)
```

- check what's in the data

```python

listobs(vis=CONT, overwrite=True, listfile='listobs_cont.txt')
```

```python
flagdata(vis=CONT, mode='list', inpfile='ek048d.flag', reason='any', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=GATE, mode='list', inpfile='ek048d.flag', reason='any', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=CONT, mode='manual', antenna='IR', correlation='RR', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=GATE, mode='manual', antenna='IR', correlation='RR', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=CONT, mode='manual', antenna='NT', spw='4', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=GATE, mode='manual', antenna='NT', spw='4', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=CONT, mode='manual', antenna='WB', spw='15', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=GATE, mode='manual', antenna='WB', spw='15', action='apply',
flagbackup=True, savepars=False)
flagdata(vis=CONT, mode='manual', spw='*:0~3;60-63', action='apply',
flagbackup=True, savepars=False)

# apriori amplitude calibration
gencal(vis=CONT, caltable='cal.tsys', caltype='tsys', uniform=False)
gencal(vis=CONT, caltable='cal.gcal', caltype='gc')

# TEC corrections
from casatasks.private import tec_maps
tec_image, tec_rms_image, plotname = tec_maps.create(vis=CONT, doplot=True)
gencal(vis=CONT, caltable='cal.tecim', caltype='tecim', infile=tec_image)
#

# take a look at phases of fringe finder 
plotms(vis=CONT, gridrows=2, gridcols=4, xaxis='channel', yaxis='amp', field='J0530+1331', timerange='15:02:00.0~15:03:00.0', avgtime='60', iteraxis='spw', coloraxis='baseline', correlation='RR, LL')

# manual fringe fit
fringefit(vis=CONT, caltable='cont.sbd', timerange='15:02:00.0~15:03:00.0', solint='inf', zerorates=True, refant='EF', minsnr=10, gaintable=['cal.gcal', 'cal.tsys'], interp=['nearest','nearest,nearest'], parang=True)

# apply single band delay corrections
applycal(vis=CONT, gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd'], interp=['nearest','nearest,nearest'], parang=True)

# plot results
plotms(vis=CONT, gridrows=2, gridcols=4, xaxis='channel', yaxis='phase', field='J0530+1331', timerange='15:02:00.0~15:03:00.0', avgtime='60', iteraxis='spw', coloraxis='baseline', correlation='RR, LL', ydatacolumn='corrected')

# global fringe fitting
fringefit(vis=CONT, caltable='cont.mbd', field='J0502+2516, J0530+1331', solint='120s', zerorates=False, refant='EF', minsnr=7, combine='spw', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd'], interp=['nearest','nearest,nearest'], parang=True)

# apply fringe fit calibration
applycal(vis=CONT, field='J0502+2516, J0530+1331', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd'], interp=['nearest','nearest,nearest', 'nearest', 'linear'], parang=True, spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

# create bandpass calibration
bandpass(vis=CONT, caltable='cont.bpass', field='J0530+1331', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd'], interp=['nearest','nearest,nearest', 'nearest', 'linear'], solnorm=True, solint='inf', refant='EF', bandtype='B', spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], parang=True, minblperant=1)

# plot the bandpass
plotms(vis='cont.bpass', xaxis='frequency', yaxis='amp', coloraxis='corr', iteraxis='antenna', gridrows=2, gridcols=4)

# apply calibration to phase calibrator and check source
applycal(vis=CONT, field='J0502+2516, J0501+2530', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd', 'cont.bpass'], interp=['nearest','nearest,nearest', 'nearest', 'linear', 'nearest,nearest'], parang=True, spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[]])

# plot calibrated phases
plotms(vis=CONT, gridrows=4, gridcols=4, xaxis='channel', yaxis='phase', field='J0502+2516', avgtime='60', iteraxis='scan', coloraxis='corr', correlation='RR, LL', ydatacolumn='corrected', avgchannel='4')

# split out phase cal and check source
split(vis=CONT, outputvis='pcal.ms', field='J0502+2516', correlation='RR, LL', datacolumn='corrected', keepflags=False, width='4', timebin='32s')
split(vis=CONT, outputvis='chksrc.ms', field='J0501+2530', correlation='RR, LL', datacolumn='corrected', keepflags=False, width='4', timebin='32s')

# image phase calibrator, limiting ourselves to the Eff-baselines
tclean(vis=PCAL, field='J0502+2516', imagename='pcal_scan4.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=128, cell='5mas', weighting='natural', niter=100, interactive=True, savemodel='modelcolumn', restart=True, antenna='5&0; 5&1; 5&2; 5&3; 5&4', scan='4, 38, 78')

# image check source, we restrict ourselves to all Eff-baselines
tclean(vis=CHKSRC, imagename='chksrc.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=128, cell='5mas', weighting='natural', niter=100, interactive=True, savemodel='modelcolumn', restart=False, antenna='5&0; 5&1; 5&2; 5&3; 5&4')

# apply calibration to target
applycal(vis=GATE, field='R67_D', gaintable=['cal.gcal', 'cal.tsys', 'cont.sbd', 'cont.mbd', 'cont.bpass'], interp=['nearest','nearest,nearest', 'nearest', 'linear', 'nearest,nearest'], parang=True, spwmap=[[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[]])

# get dirty image for all bursts individually, only on Eff baselines
for i in range(1,14):tclean(vis=GATE, scan=str(i), imagename='burst'+str(i)+'.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=1024, cell='5mas', weighting='natural', niter=0, savemodel='modelcolumn', restart=False, antenna='5&0; 5&1; 5&2; 5&3; 5&4')

# get dirty image of combined scans, skip scan 5, only Eff baselines
tclean(vis=GATE, scan='1~4,6~13', imagename='burst_all_but5.image', specmode='mfs', nterms=1, deconvolver='hogbom', gridder='standard', imsize=1024, cell='5mas', weighting='natural', niter=0, savemodel='modelcolumn', restart=False, antenna='5&0; 5&1; 5&2; 5&3; 5&4'
```
- plots to add:
  - dirty image of combined bursts
  - dirty image of first burst
  - clean image of check source
  - clean image of pcal?
  - example of calibrated phases
  - example of bandpass
---

_Content built by Franz Kirsten._ <i><span id="lastModified"></span></i>

_Built with ♥ — Markdown + HTML + CSS + Prism.js + a bit of AI + Jack Radcliffe (2025)_

<!-- Custom Script: funcs.js -->
<script>
    const copy = (el) => {
      const pre = document.querySelector(el);
      if (!pre) return;
      const code = pre.innerText;
      navigator.clipboard.writeText(code).then(() => {
        const btn = document.querySelector(`[data-copy="${el}"]`);
        if (!btn) return;
        const old = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => (btn.textContent = old), 1500);
      });
    };
    document.addEventListener('click', (e) => {
      const t = e.target;
      if (t.matches('.copy-btn')) {
        const target = t.getAttribute('data-copy');
        copy(target);
      }
    });
</script>
