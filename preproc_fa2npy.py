#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, sys
from Bio import SeqIO
from Bio.Alphabet import IUPAC
import numpy as np

def readFasta(fastaFile):

    raw_list_seq=[]
    raw_list_id=[]
    proc_list_seq = []

    for fa in SeqIO.parse(fastaFile,"fasta",alphabet=IUPAC.unambiguous_dna): # reads one fasta record at a time

        fa_id = fa.id # id
        fa_seq = str(fa.seq.upper()) # sequence

        raw_list_id.append(fa_id)
        raw_list_seq.append(fa_seq) # sequence to list

    for i in range(0,len(raw_list_seq)/2):

        id1 = raw_list_id[i*2]
        id2 = raw_list_id[i*2+1]
        seq1 = raw_list_seq[i*2]
        seq2 = raw_list_seq[i*2+1]

        ### sanity check
        if not id1.split("__")[0]+id1.split("__")[1]+id1.split("__")[2] == id2.split("__")[0]+id2.split("__")[1]+id2.split("__")[2]:
            print "3'SS ID does not match 5'SS ID", id1, id2
            sys.exit(1)

        if "3acc" in id1 and "5don" in id2:
            proc_list_seq.append(seq1+seq2)
        else:
            print "Incompatible order 3'SS===EXON===5'SS found", id1, id2
            sys.exit(1)

    return proc_list_seq

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
    print "NT Mapping:",nt_idx

    maxlen = max(map(len, list_seq)) # apply len to all seq, find max length
    X = np.zeros((len(list_seq), maxlen, len(nt_idx)), dtype=np.uint8) # set array of zeros with dim: n_sample, seq_length, 4 NT

    ### one-hot encoding
    for i, seq in enumerate(list_seq):
        for j, nuc in enumerate(seq):
            if nuc != 'N':
                X[i,j,nt_idx[nuc]] = 1
    return X

def fa2npy(fa_file, npy_file):

    X=dna_onehot_encoding(readFasta(fa_file))

    print X.shape
    print X

    np.save(npy_file,X)

    print "File",npy_file,"Saved"
    print "Done"

parser = argparse.ArgumentParser(description='FA to NPY')
parser.add_argument('-i','--input', help='input file',required=True)
parser.add_argument('-o','--output',help='output file', required=True)
args = parser.parse_args()

fa2npy(args.input, args.output)