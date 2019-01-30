import argparse

def gtf2bed(input_gtf_file, s): ## gencode v19

    span = int(s)
    transcript_dict = {}

    with open(input_gtf_file, 'r') as f:
        for line in f.readlines():
            if not line.startswith("#"):

                # read an exon and parse information
                line_tab = line.strip().split("\t")

                if line_tab[2]=="exon":
                    # print line.strip()
                    # gene level
                    chr = line_tab[0]
                    pos_start = line_tab[3]
                    pos_end = line_tab[4]
                    strand = line_tab[6]
                    info = line_tab[8]

                    # gene_id = info.split(";")[0].strip().split(" ")[1].strip("\"")
                    # transcript_id = info.split(";")[1].strip().split(" ")[1].strip("\"")
                    gene_type = info.split(";")[2].strip().split(" ")[1].strip("\"")
                    gene_status = info.split(";")[3].strip().split(" ")[1].strip("\"")
                    # gene_name = info.split(";")[4].strip().split(" ")[1].strip("\"")
                    transcript_type = info.split(";")[5].strip().split(" ")[1].strip("\"")
                    transcript_status = info.split(";")[6].strip().split(" ")[1].strip("\"")
                    transcript_name = info.split(";")[7].strip().split(" ")[1].strip("\"")
                    # exon_number = info.split(";")[8].strip().split(" ")[1]
                    exon_id = info.split(";")[9].strip().split(" ")[1].strip("\"")
                    level = info.split(";")[10].strip().split(" ")[1]

                    if gene_type=="protein_coding" and gene_status=="KNOWN" and transcript_type=="protein_coding" and transcript_status=="KNOWN" and level!="3":
                        # print gene_id,transcript_id,gene_type,gene_status,gene_name,transcript_type,transcript_status,transcript_name,exon_number,exon_id,level

                        # make uniq id for each transcript
                        tid = transcript_name+"_"+chr+"_"+strand

                        # make dict mapping id to list of exon tuple
                        if not tid in transcript_dict:
                            transcript_dict[tid] = []

                        if strand == "+":
                            transcript_dict[tid].append([pos_start,pos_end,exon_id])
                        else:
                            transcript_dict[tid].insert(0,[pos_start,pos_end,exon_id]) # if negative strand, insert at the beginning

    for t in transcript_dict:

        gene = t.split("_")[0].split("-")[0]
        chr = t.split("_")[1]
        strand = t.split("_")[2]

        txn = transcript_dict[t]

        if len(txn) > 2: # for transcript that has more than 2 exon
            for i,e in enumerate(transcript_dict[t]): # for each exon in
                if i!=0 and i!=len(txn)-1: # skip 1st exon and last exon

                    pos_start=int(e[0])
                    pos_end=int(e[1])
                    exon_id=e[2]
                    exon=chr+":"+e[0]+"-"+e[1]

                    if strand == "+":
                        print chr +"\t"+ str(pos_start-span-1) +"\t"+ str(pos_start+span-1) +"\t"+exon_id+"\t"+gene+"__3acc__intron-3pss["+exon+"]"+"\t"+strand
                        print chr +"\t"+ str(pos_end-span) +"\t"+ str(pos_end+span) +"\t"+exon_id+"\t"+gene+"__5don__["+exon+"]5pss-intron"+"\t"+strand

                    elif strand == "-":
                        print chr +"\t"+ str(pos_start-span-1) +"\t"+ str(pos_start+span-1) +"\t"+exon_id+"\t"+gene+"__5don__intron-5pss["+exon+"]"+"\t"+strand
                        print chr +"\t"+ str(pos_end-span) +"\t"+ str(pos_end+span) +"\t"+exon_id+"\t"+gene+"__3acc__["+exon+"]3pss-intron"+"\t"+strand

parser = argparse.ArgumentParser(description='GTF to BED')
parser.add_argument('-i','--input', help='input',required=True)
parser.add_argument('-s','--span',help='span', required=True)
args = parser.parse_args()

gtf2bed(args.input, args.span)