import numpy as np
import os
import sys

run = sys.argv[1]
max_evt = int(sys.argv[2])
nfiles = int(sys.argv[3]) 

evt_list = np.array_split(np.arange( max_evt), nfiles )
program ="python /reg/d/psdm/cxi/cxilp6715/scratch/bin/BAD"

for i,evts in enumerate(evt_list):
    evt_start = evts[0]
    n_evts = len( evts)

    logfile = "/reg/d/psdm/cxi/cxilp6715/scratch/logs/run%s_%d.log"%(run,i)
    
    fname = "/reg/d/psdm/cxi/cxilp6715/scratch/bigazzdata/run%s_%d.hdf5"%(run,i)

    cmd = ["bsub",
        "-o %s"%logfile,
        "-q psanaq",
        program,  
        "-r %s"%run,
        "-s %d"%evt_start,
        "-f %s"%fname,
        "-m %d"%n_evts]

    cmd = " ".join( cmd)

    os.system(cmd)

