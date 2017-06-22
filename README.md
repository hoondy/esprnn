# ESPRNN: Epigenome-based Splicing Prediction using Recurrent Neural Network

## Dependencies:
* Theano http://deeplearning.net/software/theano/
* Keras https://github.com/fchollet/keras
* NumPy http://www.numpy.org/
* scikit-learn http://scikit-learn.org/stable/
* Biopython http://biopython.org/
* (optional) matplotlib http://matplotlib.org/

## Usage Examples

### EXON definition and expression file to NPY
```
python preproc_exon2bed.py -i RNAseq.exon.RPKM.pc -s 50 -e XXX > XXX_exonDef_ss_50.bed
python preproc_bed2npy.py -i XXX_exonDef_ss_50.bed -o XXX-EXP.exonDef_ss_50.npy
```

### HG19 human genome to NPY
```
bedtools getfasta -fi hg19.fa -bed XXX_exonDef_ss_50.bed -s -name -fo XXX_exonDef_ss_50.fa
python preproc_fa2npy.py -i XXX_exonDef_ss_50.fa -o XXX-DNA.exonDef_ss_50.npy
```

### BigWig signal files to NPY
```
bwtool extract bed XXX.pval.signal.bigwig XXX.exonDef_ss_50.matrix
python preproc_matrix2npy.py -i XXX.exonDef_ss_50.matrix -o XXX.exonDef_ss_50.npy -m 2
```
