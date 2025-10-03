from casavlbitools import fitsidi
from natsort import natsort_keygen
import glob
cont_idifiles = sorted(glob.glob('ek048d_1_*IDI*'), key=natsort_keygen())
gate_idifiles = sorted(glob.glob('ek048d_2_*IDI*'), key=natsort_keygen())
try:
    fitsidi.append_tsys('ek048d.antab', cont_idifiles)
except:
    pass
try:
    fitsidi.append_gc('ek048d.antab', cont_idifiles[0])
except:
    pass
try:
    fitsidi.append_tsys('ek048d.antab', gate_idifiles)
except:
    pass
try:
    fitsidi.append_gc('ek048d.antab', gate_idifiles[0])
except:
    pass
fitsidi.convert_flags('ek048d.uvflg', cont_idifiles, outfile='ek048d.flag')
