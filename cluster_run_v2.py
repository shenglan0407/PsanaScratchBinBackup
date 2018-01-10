#!/reg/g/psdm/sw/external/python/2.7.10/x86_64-rhel7-gcc48-opt/bin/python2.7
import sys
import os
import psana
import numpy as np
import matplotlib.pyplot as plt
import scipy
import h5py
import tables
import argparse
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance
from scipy import signal
from loki.RingData import RadialProfile

###################
# Parse arguments #
###################
parser = argparse.ArgumentParser(description='Data grab')
parser.add_argument('-r', '--run', type=int, required=True, help='run number to process')
parser.add_argument('-m', '--maxcount', type=int, default=None, help='max shots to process')
args = parser.parse_args()
run = args.run

#################################
# Get radial profile file/table #
#################################
table_name = '/reg/d/psdm/cxi/cxilp6715/scratch/combined_tables/run%(key)s.tbl' % {'key' : run,}
#   minimium and maximum radii for calculating radial profile
#rmin = 150 #50 # pixel units
#rmax = 800 #1110
print("Loading data")
f = tables.File(table_name, 'r')
rads = f.root.radial_profs[:]
resampled_rads = scipy.signal.resample(rads,10)
#plot radial profile
#for i in range( 0,len(rads),1000):
#    plt.plot(rads[i], 'b')
#plt.show()

###############
# Cluster now #
###############
lgth = len(resampled_rads)
step = 1000
for i in range ( 0,lgth,step):
    print("About to cluster %s / %s ...") % (i, lgth)
    lower = i
    upper = i + step
    mat = 1 - distance.cdist( resampled_rads[lower:upper], resampled_rads[lower:upper], 'cosine')
    a = DBSCAN( eps=.02, min_samples=1).fit(mat)
    core_samples_mask = np.zeros_like(a.labels_, dtype=bool)
    core_samples_mask[a.core_sample_indices_] = True
    labels = a.labels_
    nc = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of cluster: %d' % nc)
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
        for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
       # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = mat[class_member_mask & core_samples_mask]
    
        plt.figure(1)
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        plt.figure(2)
        for r_p in  resampled_rads[labels==k]:
            plt.plot( r_p, c=col)

    plt.title('Estimated number of clusters: %d' % nc)
    plt.show()

