#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2019"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse

parser = argparse.ArgumentParser(description='GTF to BED')

parser.add_argument('-i','--input', help='input GTF',required=True)
parser.add_argument('-o','--output', help='output BED',required=True)

args = parser.parse_args()

def gtf2bed(gtf_input,bed_output):

    exon_dict={}

    with open(gtf_input,'r') as g:
        for idx,line in enumerate(g.readlines()):
            if line.startswith("#"):
                continue
            else:

                col=line.strip().split("\t")
                chromosome=col[0]
                category=col[2]
                start=col[3]
                end=col[4]
                strand=col[6]
                extra=col[8].split(";")

                if category=="exon":

                    gene_id=extra[0].strip().split(" ")[1].strip("\"")
                    transcript_id=extra[1].strip().split(" ")[1].strip("\"")

                    gene_type=extra[2].strip().split(" ")[1].strip("\"")
                    gene_status=extra[3].strip().split(" ")[1].strip("\"")
                    gene_name=extra[4].strip().split(" ")[1].strip("\"")

                    transcript_type=extra[5].strip().split(" ")[1].strip("\"")
                    transcript_status=extra[6].strip().split(" ")[1].strip("\"")
                    transcript_name=extra[7].strip().split(" ")[1].strip("\"")

                    exon_number=extra[8].strip().split(" ")[1].strip("\"")
                    exon_id=extra[9].strip().split(" ")[1].strip("\"")
                    level=extra[10].strip()

                    if gene_type=="protein_coding" and gene_status=="KNOWN" and transcript_type=="protein_coding" and transcript_status=="KNOWN" and level!="level 3":

                        if transcript_name in exon_dict:
                            exon_dict[transcript_name].append((chromosome,start,end,transcript_name+"_"+exon_id,strand))
                        else:
                            exon_dict[transcript_name] = [(chromosome,start,end,transcript_name+"_"+exon_id,strand)]

    with open(bed_output,'w') as out:
        for tx in exon_dict:
            if len(exon_dict[tx])>2:
                transcript=exon_dict[tx]

                # remove first and last exon
                for exon in transcript[1:-1]:
                    out.write(exon[0]+"\t"+exon[1]+"\t"+exon[2]+"\t"+exon[3]+"\t.\t"+exon[4]+"\n")

    print("DONE!")

gtf2bed(args.input, args.output)