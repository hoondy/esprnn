module load BEDTools
module load SAMtools

PATH_IN=$1
PREFIX=$2
ANNOTATION=$3
THREAD="4"

### NOTE: use version sorting for ALL bed files (sort -k1,1V -k2,2n), since SAM/BAM is sorted in that way.

## SORT ANNOTATION
echo "sort exon annotation"
sort -k1,1V -k2,2n --parallel=$THREAD $ANNOTATION > "$PREFIX"exon-annotation.bed

## JUNCTION
echo "make junctions"
awk 'BEGIN{OFS="\t"}{print $1, $2-20-1, $3+20,"JUNCBJ"NR, $7, ($4==1)? "+":"-",$2-20-1, $3+20,"255,0,0", 2, "20,20", "0,300" }' "$PATH_IN""$PREFIX"SJ.out.tab | sort -k1,1V -k2,2n --parallel=$THREAD > "$PREFIX"junctions.bed

echo "get left and right boundary"
sed 's/,/\t/g' "$PREFIX"junctions.bed | awk 'BEGIN{OFS="\t"}{print $1,$2,$2+$13,$4,$5,$6}' > "$PREFIX"left.bed
sed 's/,/\t/g' "$PREFIX"junctions.bed | awk 'BEGIN{OFS="\t"}{print $1,$3-$14,$3,$4,$5,$6}' > "$PREFIX"right.bed

echo "calc left and right overlap"
bedtools intersect -u -s -a "$PREFIX"left.bed -b "$PREFIX"exon-annotation.bed > "$PREFIX"left.overlap
bedtools intersect -u -s -a "$PREFIX"right.bed -b "$PREFIX"exon-annotation.bed > "$PREFIX"right.overlap

echo "concat left and right overlap"
cat "$PREFIX"left.overlap "$PREFIX"right.overlap | cut -f4 | sort --parallel=$THREAD | uniq -c | awk '{ if($1==2) print $2 }' > "$PREFIX"filtered_junctions.txt

echo "filter junctions"
grep -F -f "$PREFIX"filtered_junctions.txt "$PREFIX"junctions.bed > "$PREFIX"filtered_junctions.bed

echo "convert to intron"
sed 's/,/\t/g' "$PREFIX"filtered_junctions.bed | grep -v description | awk '{OFS="\t"}{print $1,$2+$13,$3-$14,$4,$5,$6}' > "$PREFIX"intron.bed

## EXON INC
echo "calc exon inclusion"
samtools view -@ $THREAD -L "$PREFIX"exon-annotation.bed -hb "$PATH_IN""$PREFIX"Aligned.out.sam | bedtools bamtobed -i - | sort -k1,1V -k2,2n --parallel=$THREAD > "$PREFIX"filtered_reads.bed
bedtools coverage -a "$PREFIX"exon-annotation.bed -b "$PREFIX"filtered_reads.bed -split -sorted | awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$3-$2,$4,$7}' | sort -k 5 --parallel=$THREAD > "$PREFIX"exonic_parts.inclusion

## EXON EXC
echo "calc exon exclusion"
bedtools intersect -wao -f 1.0 -s -a "$PREFIX"exon-annotation.bed -b "$PREFIX"intron.bed | awk 'BEGIN{OFS="\t"}{$13==0? s[$4]+=0:s[$4]+=$11}END{for (i in s){print i,s[i]}}' | sort -k 1 --parallel=$THREAD > "$PREFIX"exonic_parts.exclusion

## PSI
echo "calc psi"
readLength=$(grep -v "^@" -m 1 "$PATH_IN""$PREFIX"Aligned.out.sam | awk '{print length($10)}')
echo $readLength
paste "$PREFIX"exonic_parts.inclusion "$PREFIX"exonic_parts.exclusion | awk -v len="$readLength" 'BEGIN{OFS="\t"; print "exon_ID","length","inclusion","exclusion","PSI"}{NIR=$6/($4+len-1); NER=$8/(len-1)}{print $5,$4,$6,$8,(NIR+NER<=0)? "NA":NIR/(NIR+NER)}' > "$PREFIX"exonic_parts.psi

## clean
rm "$PREFIX"junctions.bed "$PREFIX"left.bed "$PREFIX"right.bed "$PREFIX"left.overlap "$PREFIX"right.overlap "$PREFIX"filtered_junctions.txt "$PREFIX"filtered_junctions.bed "$PREFIX"intron.bed "$PREFIX"exonic_parts.inclusion "$PREFIX"exonic_parts.exclusion "$PREFIX"filtered_reads.bed "$PREFIX"exon-annotation.bed

echo "DONE!"