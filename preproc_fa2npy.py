#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2019"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse
from Bio import SeqIO
from Bio.Alphabet import IUPAC
import numpy as np

parser = argparse.ArgumentParser(description='FA to NPY')
parser.add_argument('-i','--input', help='input file',required=True)
parser.add_argument('-p','--prefix',help='output prefix', required=True)
args = parser.parse_args()

def readFasta(fastaFile):

    list_id=[]
    list_seq = []

    for fa in SeqIO.parse(fastaFile,"fasta",alphabet=IUPAC.unambiguous_dna): # reads one fasta record at a time

        list_id.append(fa.id) # id
        list_seq.append(str(fa.seq.upper())) # sequence

    with open(args.prefix+'.txt','w') as o:
        for x in list_id:
            o.write(x+'\n')

    return list_seq

def dna_onehot_encoding(list_seq):

    # Input:
    # list_seq: list of sequences

    ### initialize

    # sequence to long string
    # str_seq = ""
    # for s in list_seq:
    #     str_seq=str_seq+s

    # nucleotide mapping
    # nt = set(str_seq)
    # nt_idx = {c: i for i, c in enumerate(nt)}

    nt_idx = {'A': 0, 'C': 1, 'T': 2, 'G': 3}
    print("NT Mapping:",nt_idx)

    maxlen = max(map(len, list_seq)) # apply len to all seq, find max length
    X = np.zeros((len(list_seq), maxlen, len(nt_idx)), dtype=np.uint8) # set array of zeros with dim: n_sample, seq_length, 4 NT

    ### one-hot encoding
    for i, seq in enumerate(list_seq):
        for j, nuc in enumerate(seq):
            if nuc in nt_idx.keys():
                X[i,j,nt_idx[nuc]] = 1
    return X

def fa2npy(fa_file, npy_file):

    X=dna_onehot_encoding(readFasta(fa_file))

    print(X.shape)
    print(X)

    np.savez(npy_file,X)

    print("File",npy_file,"Saved")
    print("Done")

fa2npy(args.input, args.prefix+'.npz')