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

def bed2npy(bed_file, npy_file):

    raw_list_cat=[]
    raw_list_id=[]
    proc_list_cat = []

    with open(bed_file, 'r') as f:
        for line in f.readlines():
            line_split = line.rstrip().split("\t")
            raw_list_id.append(line_split[3])
            raw_list_cat.append(line_split[4])

    for i in range(0,len(raw_list_cat)/2):

        id1 = raw_list_id[i*2]
        id2 = raw_list_id[i*2+1]
        cat1 = raw_list_cat[i*2]
        cat2 = raw_list_cat[i*2+1]

         ### sanity check
        if not id1.split("__")[0]+id1.split("__")[1]+id1.split("__")[2] == id2.split("__")[0]+id2.split("__")[1]+id2.split("__")[2]:
            print("3'SS ID does not match 5'SS ID", id1, id2)
            sys.exit(1)

        if cat1 == cat2:
            proc_list_cat.append(int(cat1))
        else:
            print("ID1 != ID2", id1, id2)
            sys.exit(1)

    Y = np.zeros((len(proc_list_cat), len(set(proc_list_cat))), dtype=np.uint8)
    for i, seq in enumerate(proc_list_cat):
        Y[i, proc_list_cat[i]] = 1

    print(Y.shape)
    print(Y)
    np.save(npy_file,Y)

    print("File",npy_file,"Saved")
    print("Done")

parser = argparse.ArgumentParser(description='BED to NPY')
parser.add_argument('-i','--input', help='input file',required=True)
parser.add_argument('-o','--output',help='output file', required=True)
args = parser.parse_args()

bed2npy(args.input, args.output)