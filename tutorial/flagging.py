CONT='ek048d_cont.ms'
GATE='ek048d_gate.ms'
MSs = [CONT, GATE]
for MS in MSs:
    flagdata(vis=MS, mode='list', inpfile='ek048d.flag', reason='any', action='apply', flagbackup=True, savepars=False)
    flagdata(vis=MS, mode='manual', antenna='IR', correlation='RR', action='apply', flagbackup=True, savepars=False)
    flagdata(vis=MS, mode='manual', antenna='NT', spw='4', action='apply', flagbackup=True, savepars=False)
    flagdata(vis=MS, mode='manual', antenna='WB', spw='15', action='apply', flagbackup=True, savepars=False)
    flagdata(vis=MS, mode='manual', spw='*:0~3;60~63', action='apply', flagbackup=True, savepars=False)
    flagdata(vis=MS, mode='manual', autocorr=True, action='apply', flagbackup=True, savepars=False)
