#!/reg/g/psdm/sw/external/python/2.7.10/x86_64-rhel7-gcc48-opt/bin/python2.7
import sys
import os

import numpy as np
import h5py
import argparse
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

import psana
from scipy.spatial import distance
import matplotlib.pyplot as plt
from loki.RingData import RadialProfile

parser = argparse.ArgumentParser(description='Data grab')
parser.add_argument('-r', '--run', type=int, required=True, help='run number to process')
parser.add_argument('-m', '--maxcount', type=int, default=None, help='max shots to process')
args = parser.parse_args()
run = args.run

data_fname = '/reg/d/psdm/cxi/cxilp6715/scratch/analysis/run%(key)s/small_data-%(key)s.hdf5' % {'key' : run,}
cent_fname = '/reg/data/ana14/cxi/cxilp6715/scratch/bin/center.npy'
mask_fname = '/reg/data/ana14/cxi/cxilp6715/scratch/bin/mask_rough.npy'
#   point where forward beam intersects detector
cent = np.load( cent_fname)
mask = np.load( mask_fname) 

img_sh = mask.shape

#   minimium and maximum radii for calculating radial profile
rmin = 150 #50 # pixel units
rmax = 800 #1110

rp = RadialProfile( cent, img_sh, mask)


print("Loading data")
f = h5py.File(data_fname, 'r')
dat=f['assembled']


print("Computing the radial profiles")
radprof =np.array(  [ rp.calculate(img)[rmin:rmax] for img in dat] )

#plot radial profile
#for i in range( 0,len(radprof),10):
#    plt.plot(radprof[i], 'b')
#plt.show()


print("About to cluster...")
# CLUSTERING NOW #
mat = 1 - distance.cdist( radprof[:], radprof[:], 'cosine')
a = DBSCAN( eps=.013, min_samples=1).fit(mat)
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
    for r_p in  radprof[labels==k]:
        plt.plot( r_p, c=col)

    #xy = mat[class_member_mask & ~core_samples_mask]i
    #plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #         markeredgecolor='k', markersize=6)
plt.title('Estimated number of clusters: %d' % nc)
plt.show()

#plot radial profiles colored by cluster
#for i in range( 0,len(radprof),10):
#    plt.plot(radprof[i], 'b')
#plt.show()





