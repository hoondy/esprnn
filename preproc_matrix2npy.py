#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, sys
import numpy as np
from sklearn import preprocessing

def matrix2npy(matrix_file, npy_file, max_cutoff):

    raw_list_mat=[]
    raw_list_id=[]
    proc_list_mat = []

    with open(matrix_file, 'r') as f:
        for line in f.readlines():
            line_split = line.rstrip().split("\t")
            raw_list_id.append(line_split[3])

            # convert NA to 0
            list_val = list(line_split[7].split(","))
            list_val = [0 if (x=="NA") else x for x in list_val]

            # reverse if negative strand
            strand = line_split[5]
            if strand == "-":
                list_val.reverse()

            # add to raw list
            raw_list_mat.append(list_val)

    for i in range(0,len(raw_list_mat)/2):

        id1 = raw_list_id[i*2]
        id2 = raw_list_id[i*2+1]
        seq1 = raw_list_mat[i*2]
        seq2 = raw_list_mat[i*2+1]

        ### sanity check
        if not id1.split("__")[0]+id1.split("__")[1]+id1.split("__")[2] == id2.split("__")[0]+id2.split("__")[1]+id2.split("__")[2]:
            print "3'SS ID does not match 5'SS ID", id1, id2
            sys.exit(1)

        if "3acc" in id1 and "5don" in id2:
            proc_list_mat.append(seq1+seq2)
        else:
            print "Incompatible order 3'SS===EXON===5'SS found", id1, id2
            sys.exit(1)

    maxlen = max(map(len, proc_list_mat)) # apply len to all seq, find max length

    X = np.zeros((len(proc_list_mat), maxlen, 1), dtype=np.float_) # set array of zeros with dim: n_sample, seq_length, 4 NT
    for i, seq in enumerate(proc_list_mat):
        for j, val in enumerate(seq):
            if max_cutoff:
                if float(val)>=float(max_cutoff):
                    X[i,j,0]=float(max_cutoff)
                else:
                    X[i,j,0]=float(val)
            else:
                X[i,j,0]=float(val)
        # print X[i,:,0]

    # scale data to [0,1]
    min_max_scaler = preprocessing.MinMaxScaler()
    X[:,:,0] = min_max_scaler.fit_transform(X[:,:,0])

    print X.shape
    print X

    np.save(npy_file,X)

    print "File",npy_file,"Saved"
    print "Done"

parser = argparse.ArgumentParser(description='MATRIX to NPY')
parser.add_argument('-i','--input', help='input file',required=True)
parser.add_argument('-o','--output',help='output file', required=True)
parser.add_argument('-m','--max',help='max cutoff', required=False)
args = parser.parse_args()

matrix2npy(args.input, args.output, args.max)