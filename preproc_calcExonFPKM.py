#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2018, Gerstein Lab"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, os
import numpy as np

parser = argparse.ArgumentParser(description='parser')
parser.add_argument('-p', '--path', help='path to files', required=True)
parser.add_argument('-s', '--sample', help='sample name to merge', required=True)
parser.add_argument('-a', '--acc', help='accession id to merge', required=False)
parser.add_argument('-l', '--length', help='exon length', required=True)
parser.add_argument('-o', '--output', help='output', required=True)
args = parser.parse_args()

# read exon length
print "Loading exon length file..."
exon_length={}
with open(args.length, 'r') as f:
    for idx,line in enumerate(f.readlines()):
        # print line.strip()
        eid = line.strip().split("\t")[0]
        elength = line.strip().split("\t")[1]
        exon_length[eid]=elength

# find all files corresponding to sample name
files2process = []
for f in os.listdir(args.path):
    if args.acc:
        if args.acc in f and f.endswith(".tsv"):
            print "Matching by accession:",args.acc
            print "Found",f
            files2process.append(os.path.join(args.path, f))
    else:
        if args.sample in f and f.endswith(".tsv"):
            print "Matching by sample:",args.sample
            print "Found",f
            files2process.append(os.path.join(args.path, f))
num_rep = len(files2process)

print "Merging",num_rep,"files..."

exon_id=[]
exon_count={}
total_num_reads=[]
for file in files2process:
    print "Loading",file
    total_read_count=0
    with open(file, 'r') as f:
        for idx,line in enumerate(f.readlines()):
            if not line.startswith("__"):
                eid = line.strip().split("\t")[0]
                gene = line.strip().split("\t")[1]
                read_count = line.strip().split("\t")[2]

                total_read_count+=int(read_count)

                if exon_count.has_key(eid):
                    exon_count[eid].append(read_count)
                else:
                    exon_count[eid]=[read_count]
        total_num_reads.append(total_read_count)
# print total_num_reads

with open(args.output, 'w') as out:
    if args.acc:
        out.write("exon_id\t"+args.sample+"_"+args.acc+"\n")
    else:
        out.write("exon_id\t"+args.sample+"\n")
    for i,eid in enumerate(sorted(exon_count.keys())):
        if exon_length.has_key(eid):
            li=int(exon_length[eid])
            if li>0:
                fpkm=np.zeros(shape=num_rep)

                for j in range(0,num_rep):
                    xi=int(exon_count[eid][j])
                    n=int(total_num_reads[j])

                    fpkm[j]=xi * 1e9  / (li * n)
                fpkm_mean = np.mean(fpkm, axis=0)

                out.write(eid+"\t"+str('%1.4f' % fpkm_mean)+"\n")
print "DONE"