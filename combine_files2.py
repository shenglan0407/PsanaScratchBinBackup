

#run = sys.argv[1]

import os
import tables
from shutil import copyfile
import glob
import sys

def combine_files(run):

    dirpath1 = '/reg/data/ana14/cxi/cxilp6715/scratch/bigazzradialprofiles'
    dirpath2 = '/reg/data/ana14/cxi/cxilp6715/scratch/output'
    dirpath3 = '/reg/data/ana14/cxi/cxilp6715/scratch/output2'
    newfname = '/reg/data/ana14/cxi/cxilp6715/scratch/waxs/run%d.tbl'%run
    
    fnames = glob.glob(  "%s/run%d_*.hdf5"%(dirpath1, run) )
    fnames += glob.glob(  "%s/run%d_*.hdf5"%(dirpath2, run) )
    fnames += glob.glob(  "%s/run%d_*.hdf5"%(dirpath3, run) )

    print fnames
    if os.path.exists(newfname):
        return None

    if not fnames:
        print("No filenames for run %d"%run)
        return None
    
    for f in fnames:
        try:
            tables.File(f, 'r')
        except tables.exceptions.HDF5ExtError:
            print ("Cannot open file %s"%f)
            return None

#   copy first file as a start
    copyfile( fnames[0], newfname )

#   this gets every EArray path in the file (data is stored as EArrays.. 
    get_array_paths = lambda PyTable:  [s.split()[0] 
        for s in str(PyTable).split('\n') if 'EArray' in s]

#   this is the master file we will append to
    with tables.File(newfname, 'r+') as tbl:

        array_paths = get_array_paths(tbl)

#       read each file, make sure it has the same Earray fields, 
#       and then append... 
        for fname in fnames[1:]:
            next_tbl = tables.File( fname, 'r')
            next_array_paths = get_array_paths( next_tbl)
            if not all( [ path in array_paths for path in next_array_paths] ):
                print("Incomplete Pytable: %s"%fname)
                print("\tMissing the following Earrays") 
                print 0
                print next_array_paths,'\n'
                print array_paths
                print 0
                #print( [ path for path in next_array_paths if path not in array_paths] )
                os.remove(newfname)
                return None
            
            for path in next_array_paths:
                tbl.get_node(path).append( next_tbl.get_node(path)[:] ) 


runs = range( 1,95)
for r in runs:
    combine_files(r)


