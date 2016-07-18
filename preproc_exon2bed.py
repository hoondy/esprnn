#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"


### parse RPKM expression matrix
### e.g., 57epigenomes.exon.RPKM.pc: RPKM expression matrix for protein coding exons

import argparse, sys

def exon2bed(input_file, span, sample):

    span = int(span)
    transcript_dict = {}
    header_dict = {}

    with open(input_file, 'r') as f:
        for line in f.readlines():

            # split line
            line_tab = line.strip().split("\t")

            # if header line
            if "exon_location" in line:
                for i,v in enumerate(line_tab):
                    header_dict[v]=i
                # print header_dict
                continue

            exon_location=line_tab[0]
            gene_id=line_tab[1]
            rpkm=line_tab[header_dict[sample]]

            # read an exon and parse information
            pos=exon_location.split("<")[0]
            chr = pos.split(":")[0]
            pos_start = pos.split(":")[1].split("-")[0]
            pos_end = pos.split(":")[1].split("-")[1].split("<")[0]

            # strand
            # print exon_location.split("<")[1]
            if int(exon_location.split("<")[1]) == 1:
                strand="+"
            else:
                strand="-"

            # print chr,pos_start,pos_end,strand,rpkm
            # break

            # make uniq id for each transcript
            transcript_id = gene_id+"__"+chr+"__"+strand
            # print transcript_id

            # make dict mapping id to list of exon tuple
            if not transcript_id in transcript_dict:
                transcript_dict[transcript_id] = list()
            transcript_dict[transcript_id].append([pos_start,pos_end,rpkm])

    for t in transcript_dict:

        chr = t.split("__")[1]
        strand = t.split("__")[2]

        if len(transcript_dict[t]) > 2: # for transcript that has more than 2 exon, we want 3'SS-exon-5'SS

            ### flip order for reverse strand
            if strand == "+":
                transcript_dict[t] = sorted(transcript_dict[t])
            else:
                transcript_dict[t] = sorted(transcript_dict[t],reverse=True)

            ### remove first and last exon, because whole 3'SS-exon-5'SS form is needed
            del transcript_dict[t][0]
            del transcript_dict[t][-1]

            for exon in transcript_dict[t]: # for each exon in

                ### if RPKM >1 is expressed(1), otherwise unexpressed(0)
                expr = str(int(float(exon[2])>1))
                print float(exon[2])

                if strand == "+":
                    pos = int(exon[0])
                    print chr + "\t" + str(pos-span-1) + "\t" + str(pos+span-1) + "\t" + t + "__3acc__intron-3pss["+str(pos)+"-exon" + "\t" + expr + "\t" + strand

                    pos = int(exon[1])
                    print chr + "\t" + str(pos-span) + "\t" + str(pos+span) + "\t" + t + "__5don__exon-"+str(pos)+"]5pss-intron" + "\t" + expr + "\t" + strand

                else: # neg strand
                    pos = int(exon[1])
                    print chr + "\t" + str(pos-span) + "\t" + str(pos+span) + "\t" + t + "__3acc__intron-3pss["+str(pos)+"-exon" + "\t" + expr + "\t" + strand

                    pos = int(exon[0])
                    print chr + "\t" + str(pos-span-1) + "\t" + str(pos+span-1) + "\t" + t +"__5don__exon-"+str(pos)+"]5pss-intron" + "\t" + expr + "\t" + strand


parser = argparse.ArgumentParser(description='EXON to BED')
parser.add_argument('-i','--input', help='file',required=True)
parser.add_argument('-s','--span',help='span', required=True)
parser.add_argument('-e','--eid',help='sample eid', required=True)
args = parser.parse_args()

exon2bed(args.input, args.span, args.eid)
