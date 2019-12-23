#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2019"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse
import h5py
import numpy as np

parser = argparse.ArgumentParser(description='NPY to HDF5')

parser.add_argument('-d','--path', help='path to input files',required=True)
parser.add_argument('-a','--x1', help='input files for 3acc (comma separated)',required=True)
parser.add_argument('-b','--x2',help='input files for 5don (comma separated)', required=True)
parser.add_argument('-y','--y',help='input response variable', required=True)

parser.add_argument('-p','--prefix',help='output prefix', required=True)
parser.add_argument('-s','--span', help='span window size (input sequence length for each splice site)',required=False, type=int, default=400)

args = parser.parse_args()

inputFiles = list(zip(args.x1.split(","),args.x2.split(",")))
print("Found",len(inputFiles),"files")

with h5py.File(args.prefix+".hdf5", mode='w') as f:
    for idx, file in enumerate(inputFiles):
        print("Loading ",file[0],file[1])
        tmp=np.concatenate((np.load(args.path+"/"+file[0]),np.load(args.path+"/"+file[1])),axis=1)

        if idx==0:
            f.create_dataset("x", data=tmp, chunks=True, maxshape=(None,2*args.span,None), dtype='f')
        else:
            f["x"].resize((f["x"].shape[2] + tmp.shape[2]), axis = 2)
            f["x"][:,:,-tmp.shape[2]:] = tmp

        print(f['x'].shape)
    f.create_dataset("y", data=np.load(args.path+"/"+args.y), chunks=True, maxshape=(None,1))
