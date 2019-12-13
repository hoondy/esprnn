#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2019"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse
import numpy as np
from sklearn import preprocessing
import math
import pandas as pd
import pyBigWig

parser = argparse.ArgumentParser(description='BW to NPY')
parser.add_argument('-i','--bigwig', help='input bigWig file',required=True)
parser.add_argument('-b','--bed',help='bed file', required=True)
parser.add_argument('-s','--span',help='span', required=False, type=int, default=200)
parser.add_argument('-p','--prefix',help='output prefix', required=True)
args = parser.parse_args()

def sigmoid(x):
    return 1 / (1 + math.exp(-2*(x-2))) #k=2, x0=2

def bw2npy(bw_file, bed_file, npy_file):

    bw = pyBigWig.open(bw_file)
    bed=pd.read_csv(bed_file,sep='\t',header=None)

    X = np.zeros((bed.shape[0], 2*args.span, 1), dtype=np.float_) # set array of zeros with dim: n_sample, exon span, 1

    for i in range(bed.shape[0]):
        # if positive strand, store sigmoid normalized signal value
        if bed.loc[i,5]=='+':
            tmp=np.array([sigmoid(x) for x in (bw.values(bed.loc[i,0], int(bed.loc[i,1]-args.span), int(bed.loc[i,2]+args.span)))])
            np.nan_to_num(tmp)
            np.around(tmp, decimals=2)
            X[i,:,0]=tmp

        # if negative strand, reverse signal value
        else:
            tmp=np.array([sigmoid(x) for x in (bw.values(bed.loc[i,0], int(bed.loc[i,1]-args.span), int(bed.loc[i,2]+args.span)))][::-1])
            np.nan_to_num(tmp)
            np.around(tmp, decimals=2)
            X[i,:,0]=tmp

    bw.close()

    # normalize data
    min_max_scaler = preprocessing.MinMaxScaler()
    X[:,:,0] = min_max_scaler.fit_transform(X[:,:,0])

    print(X.shape)
    print(X)

    np.save(npy_file,X)

    print("File",npy_file,"Saved")
    print("Done")

bw2npy(args.bigwig, args.bed, args.prefix+".npy")