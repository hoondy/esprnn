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
parser.add_argument('-p','--prefix',help='output prefix', required=True)
parser.add_argument('-m','--max',help='max cutoff', required=False)
args = parser.parse_args()

def sigmoid(x):
    return 1 / (1 + math.exp(-2*(x-2))) #k=2, x0=2

def bw2npy(bw_file, bed_file, npy_file):

    tmp = []
    bw = pyBigWig.open(bw_file)
    bed=pd.read_csv(bed_file,sep='\t',header=None)

    for i in range(bed.shape[0]):
        # if positive strand, store sigmoid normalized signal value
        if bed.loc[i,5]=='+':
            tmp.append([sigmoid(x) for x in (bw.values(bed.loc[i,0], int(bed.loc[i,1]), int(bed.loc[i,2])))])
        # if negative strand, reverse signal value
        else:
            tmp.append([sigmoid(x) for x in (bw.values(bed.loc[i,0], int(bed.loc[i,1]), int(bed.loc[i,2])))][::-1])

    bw.close()

    maxlen = max(map(len, tmp)) # apply len to all seq, find max length

    X = np.zeros((len(tmp), maxlen, 1), dtype=np.float_) # set array of zeros with dim: n_sample, exon span, 1
    for i, seq in enumerate(tmp):
        for j, val in enumerate(seq):
            X[i,j,0]=float(val)

    # normalize data
    min_max_scaler = preprocessing.MinMaxScaler()
    X[:,:,0] = min_max_scaler.fit_transform(X[:,:,0])

    print(X.shape)
    print(X)

    np.save(npy_file,X)

    print("File",npy_file,"Saved")
    print("Done")

bw2npy(args.bigwig, args.bed, args.prefix+".npy")