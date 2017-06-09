#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import numpy as np
import sys

def loadData(EID):

    print 'Loading Data..'
    print 'EID:',EID

    if EID == "E027":

        E027_DNA = np.load("../data/npyData/E027-DNA.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E027-EXP.exonDef_ss_100.npy")
        E027_H3K27me3 = np.load("../data/npyData/E027-H3K27me3.exonDef_ss_100.npy")
        E027_H3K36me3 = np.load("../data/npyData/E027-H3K36me3.exonDef_ss_100.npy")
        E027_H3K4me1 = np.load("../data/npyData/E027-H3K4me1.exonDef_ss_100.npy")
        E027_H3K4me3 = np.load("../data/npyData/E027-H3K4me3.exonDef_ss_100.npy")
        E027_H3K9ac = np.load("../data/npyData/E027-H3K9ac.exonDef_ss_100.npy")
        E027_H3K9me3 = np.load("../data/npyData/E027-H3K9me3.exonDef_ss_100.npy")
        E027_Methylation = np.load("../data/npyData/E027-Methylation.exonDef_ss_100.npy")
        E027_CORE = np.concatenate((E027_H3K4me1,E027_H3K4me3,E027_H3K27me3,E027_H3K36me3,E027_H3K9me3),axis=2)
        E027_EXTRA = np.concatenate((E027_H3K9ac,E027_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E027_DNA,E027_CORE),axis=2)
        inputX_LONG = np.concatenate((E027_DNA,E027_CORE,E027_EXTRA),axis=2)

    elif EID == "E028":

        E028_DNA = np.load("../data/npyData/E028-DNA.exonDef_ss_100.npy")
        E028_DNase = np.load("../data/npyData/E028-DNase.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E028-EXP.exonDef_ss_100.npy")
        E028_H3K27me3 = np.load("../data/npyData/E028-H3K27me3.exonDef_ss_100.npy")
        E028_H3K36me3 = np.load("../data/npyData/E028-H3K36me3.exonDef_ss_100.npy")
        E028_H3K4me1 = np.load("../data/npyData/E028-H3K4me1.exonDef_ss_100.npy")
        E028_H3K4me3 = np.load("../data/npyData/E028-H3K4me3.exonDef_ss_100.npy")
        E028_H3K9me3 = np.load("../data/npyData/E028-H3K9me3.exonDef_ss_100.npy")
        E028_Methylation = np.load("../data/npyData/E028-Methylation.exonDef_ss_100.npy")
        E028_CORE = np.concatenate((E028_H3K4me1,E028_H3K4me3,E028_H3K27me3,E028_H3K36me3,E028_H3K9me3),axis=2)
        E028_EXTRA = np.concatenate((E028_DNase,E028_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E028_DNA,E028_CORE),axis=2)
        inputX_LONG = np.concatenate((E028_DNA,E028_CORE,E028_EXTRA),axis=2)

    elif EID == "E066":

        E066_DNA = np.load("../data/npyData/E066-DNA.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E066-EXP.exonDef_ss_100.npy")
        E066_H3K27ac = np.load("../data/npyData/E066-H3K27ac.exonDef_ss_100.npy")
        E066_H3K27me3 = np.load("../data/npyData/E066-H3K27me3.exonDef_ss_100.npy")
        E066_H3K36me3 = np.load("../data/npyData/E066-H3K36me3.exonDef_ss_100.npy")
        E066_H3K4me1 = np.load("../data/npyData/E066-H3K4me1.exonDef_ss_100.npy")
        E066_H3K4me3 = np.load("../data/npyData/E066-H3K4me3.exonDef_ss_100.npy")
        E066_H3K9ac = np.load("../data/npyData/E066-H3K9ac.exonDef_ss_100.npy")
        E066_H3K9me3 = np.load("../data/npyData/E066-H3K9me3.exonDef_ss_100.npy")
        E066_Methylation = np.load("../data/npyData/E066-Methylation.exonDef_ss_100.npy")
        E066_CORE = np.concatenate((E066_H3K4me1,E066_H3K4me3,E066_H3K27me3,E066_H3K36me3,E066_H3K9me3),axis=2)
        E066_EXTRA = np.concatenate((E066_H3K9ac,E066_H3K27ac,E066_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E066_DNA,E066_CORE),axis=2)
        inputX_LONG = np.concatenate((E066_DNA,E066_CORE,E066_EXTRA),axis=2)

    elif EID == "E096":

        E096_DNA = np.load("../data/npyData/E096-DNA.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E096-EXP.exonDef_ss_100.npy")
        E096_H3K27ac = np.load("../data/npyData/E096-H3K27ac.exonDef_ss_100.npy")
        E096_H3K27me3 = np.load("../data/npyData/E096-H3K27me3.exonDef_ss_100.npy")
        E096_H3K36me3 = np.load("../data/npyData/E096-H3K36me3.exonDef_ss_100.npy")
        E096_H3K4me1 = np.load("../data/npyData/E096-H3K4me1.exonDef_ss_100.npy")
        E096_H3K4me3 = np.load("../data/npyData/E096-H3K4me3.exonDef_ss_100.npy")
        E096_H3K9me3 = np.load("../data/npyData/E096-H3K9me3.exonDef_ss_100.npy")
        E096_Methylation = np.load("../data/npyData/E096-Methylation.exonDef_ss_100.npy")
        E096_CORE = np.concatenate((E096_H3K4me1,E096_H3K4me3,E096_H3K27me3,E096_H3K36me3,E096_H3K9me3),axis=2)
        E096_EXTRA = np.concatenate((E096_H3K27ac,E096_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E096_DNA,E096_CORE),axis=2)
        inputX_LONG = np.concatenate((E096_DNA,E096_CORE,E096_EXTRA),axis=2)

    elif EID == "E114":

        E114_DNA = np.load("../data/npyData/E114-DNA.exonDef_ss_100.npy")
        E114_DNase = np.load("../data/npyData/E114-DNase.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E114-EXP.exonDef_ss_100.npy")
        E114_H2A = np.load("../data/npyData/E114-H2A.Z.exonDef_ss_100.npy")
        E114_H3K27ac = np.load("../data/npyData/E114-H3K27ac.exonDef_ss_100.npy")
        E114_H3K27me3 = np.load("../data/npyData/E114-H3K27me3.exonDef_ss_100.npy")
        E114_H3K36me3 = np.load("../data/npyData/E114-H3K36me3.exonDef_ss_100.npy")
        E114_H3K4me1 = np.load("../data/npyData/E114-H3K4me1.exonDef_ss_100.npy")
        E114_H3K4me2 = np.load("../data/npyData/E114-H3K4me2.exonDef_ss_100.npy")
        E114_H3K4me3 = np.load("../data/npyData/E114-H3K4me3.exonDef_ss_100.npy")
        E114_H3K79me2 = np.load("../data/npyData/E114-H3K79me2.exonDef_ss_100.npy")
        E114_H3K9ac = np.load("../data/npyData/E114-H3K9ac.exonDef_ss_100.npy")
        E114_H3K9me3 = np.load("../data/npyData/E114-H3K9me3.exonDef_ss_100.npy")
        E114_H4K20me1 = np.load("../data/npyData/E114-H4K20me1.exonDef_ss_100.npy")
        E114_Methylation = np.load("../data/npyData/E114-Methylation.exonDef_ss_100.npy")
        E114_CORE = np.concatenate((E114_H3K4me1,E114_H3K4me3,E114_H3K27me3,E114_H3K36me3,E114_H3K9me3),axis=2)
        E114_EXTRA = np.concatenate((E114_H3K9ac,E114_H3K27ac,E114_H3K4me2,E114_H3K79me2,E114_H4K20me1,E114_H2A,E114_DNase,E114_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E114_DNA,E114_CORE),axis=2)
        inputX_LONG = np.concatenate((E114_DNA,E114_CORE,E114_EXTRA),axis=2)

    elif EID == "E116":

        E116_DNA = np.load("../data/npyData/E116-DNA.exonDef_ss_100.npy")
        E116_DNase = np.load("../data/npyData/E116-DNase.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E116-EXP.exonDef_ss_100.npy")
        E116_H2A = np.load("../data/npyData/E116-H2A.Z.exonDef_ss_100.npy")
        E116_H3K27ac = np.load("../data/npyData/E116-H3K27ac.exonDef_ss_100.npy")
        E116_H3K27me3 = np.load("../data/npyData/E116-H3K27me3.exonDef_ss_100.npy")
        E116_H3K36me3 = np.load("../data/npyData/E116-H3K36me3.exonDef_ss_100.npy")
        E116_H3K4me1 = np.load("../data/npyData/E116-H3K4me1.exonDef_ss_100.npy")
        E116_H3K4me2 = np.load("../data/npyData/E116-H3K4me2.exonDef_ss_100.npy")
        E116_H3K4me3 = np.load("../data/npyData/E116-H3K4me3.exonDef_ss_100.npy")
        E116_H3K79me2 = np.load("../data/npyData/E116-H3K79me2.exonDef_ss_100.npy")
        E116_H3K9ac = np.load("../data/npyData/E116-H3K9ac.exonDef_ss_100.npy")
        E116_H3K9me3 = np.load("../data/npyData/E116-H3K9me3.exonDef_ss_100.npy")
        E116_H4K20me1 = np.load("../data/npyData/E116-H4K20me1.exonDef_ss_100.npy")
        E116_Methylation = np.load("../data/npyData/E116-Methylation.exonDef_ss_100.npy")
        E116_Nucleosome = np.load("../data/npyData/E116-Nucleosome.exonDef_ss_100.npy")
        E116_CORE = np.concatenate((E116_H3K4me1,E116_H3K4me3,E116_H3K27me3,E116_H3K36me3,E116_H3K9me3),axis=2)
        E116_EXTRA = np.concatenate((E116_H3K9ac,E116_H3K27ac,E116_H3K4me2,E116_H3K79me2,E116_H4K20me1,E116_H2A,E116_DNase,E116_Methylation,E116_Nucleosome),axis=2)
        inputX_SHORT = np.concatenate((E116_DNA,E116_CORE),axis=2)
        inputX_LONG = np.concatenate((E116_DNA,E116_CORE,E116_EXTRA),axis=2)

    elif EID == "E118":

        E118_DNA = np.load("../data/npyData/E118-DNA.exonDef_ss_100.npy")
        E118_DNase = np.load("../data/npyData/E118-DNase.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E118-EXP.exonDef_ss_100.npy")
        E118_H2A = np.load("../data/npyData/E118-H2A.Z.exonDef_ss_100.npy")
        E118_H3K27ac = np.load("../data/npyData/E118-H3K27ac.exonDef_ss_100.npy")
        E118_H3K27me3 = np.load("../data/npyData/E118-H3K27me3.exonDef_ss_100.npy")
        E118_H3K36me3 = np.load("../data/npyData/E118-H3K36me3.exonDef_ss_100.npy")
        E118_H3K4me1 = np.load("../data/npyData/E118-H3K4me1.exonDef_ss_100.npy")
        E118_H3K4me2 = np.load("../data/npyData/E118-H3K4me2.exonDef_ss_100.npy")
        E118_H3K4me3 = np.load("../data/npyData/E118-H3K4me3.exonDef_ss_100.npy")
        E118_H3K79me2 = np.load("../data/npyData/E118-H3K79me2.exonDef_ss_100.npy")
        E118_H3K9ac = np.load("../data/npyData/E118-H3K9ac.exonDef_ss_100.npy")
        E118_H3K9me3 = np.load("../data/npyData/E118-H3K9me3.exonDef_ss_100.npy")
        E118_H4K20me1 = np.load("../data/npyData/E118-H4K20me1.exonDef_ss_100.npy")
        E118_Methylation = np.load("../data/npyData/E118-Methylation.exonDef_ss_100.npy")
        E118_CORE = np.concatenate((E118_H3K4me1,E118_H3K4me3,E118_H3K27me3,E118_H3K36me3,E118_H3K9me3),axis=2)
        E118_EXTRA = np.concatenate((E118_H3K9ac,E118_H3K27ac,E118_H3K4me2,E118_H3K79me2,E118_H4K20me1,E118_H2A,E118_DNase,E118_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E118_DNA,E118_CORE),axis=2)
        inputX_LONG = np.concatenate((E118_DNA,E118_CORE,E118_EXTRA),axis=2)

    elif EID == "E119":

        E119_DNA = np.load("../data/npyData/E119-DNA.exonDef_ss_100.npy")
        E119_DNase = np.load("../data/npyData/E119-DNase.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E119-EXP.exonDef_ss_100.npy")
        E119_H2A = np.load("../data/npyData/E119-H2A.Z.exonDef_ss_100.npy")
        E119_H3K27ac = np.load("../data/npyData/E119-H3K27ac.exonDef_ss_100.npy")
        E119_H3K27me3 = np.load("../data/npyData/E119-H3K27me3.exonDef_ss_100.npy")
        E119_H3K36me3 = np.load("../data/npyData/E119-H3K36me3.exonDef_ss_100.npy")
        E119_H3K4me1 = np.load("../data/npyData/E119-H3K4me1.exonDef_ss_100.npy")
        E119_H3K4me2 = np.load("../data/npyData/E119-H3K4me2.exonDef_ss_100.npy")
        E119_H3K4me3 = np.load("../data/npyData/E119-H3K4me3.exonDef_ss_100.npy")
        E119_H3K79me2 = np.load("../data/npyData/E119-H3K79me2.exonDef_ss_100.npy")
        E119_H3K9ac = np.load("../data/npyData/E119-H3K9ac.exonDef_ss_100.npy")
        E119_H3K9me3 = np.load("../data/npyData/E119-H3K9me3.exonDef_ss_100.npy")
        E119_H4K20me1 = np.load("../data/npyData/E119-H4K20me1.exonDef_ss_100.npy")
        E119_Methylation = np.load("../data/npyData/E119-Methylation.exonDef_ss_100.npy")
        E119_CORE = np.concatenate((E119_H3K4me1,E119_H3K4me3,E119_H3K27me3,E119_H3K36me3,E119_H3K9me3),axis=2)
        E119_EXTRA = np.concatenate((E119_H3K9ac,E119_H3K27ac,E119_H3K4me2,E119_H3K79me2,E119_H4K20me1,E119_H2A,E119_DNase,E119_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E119_DNA,E119_CORE),axis=2)
        inputX_LONG = np.concatenate((E119_DNA,E119_CORE,E119_EXTRA),axis=2)

    elif EID == "E123":

        E123_DNA = np.load("../data/npyData/E123-DNA.exonDef_ss_100.npy")
        E123_DNase = np.load("../data/npyData/E123-DNase.exonDef_ss_100.npy")
        inputY = np.load("../data/npyData/E123-EXP.exonDef_ss_100.npy")
        E123_H2A = np.load("../data/npyData/E123-H2A.Z.exonDef_ss_100.npy")
        E123_H3K27ac = np.load("../data/npyData/E123-H3K27ac.exonDef_ss_100.npy")
        E123_H3K27me3 = np.load("../data/npyData/E123-H3K27me3.exonDef_ss_100.npy")
        E123_H3K36me3 = np.load("../data/npyData/E123-H3K36me3.exonDef_ss_100.npy")
        E123_H3K4me1 = np.load("../data/npyData/E123-H3K4me1.exonDef_ss_100.npy")
        E123_H3K4me2 = np.load("../data/npyData/E123-H3K4me2.exonDef_ss_100.npy")
        E123_H3K4me3 = np.load("../data/npyData/E123-H3K4me3.exonDef_ss_100.npy")
        E123_H3K79me2 = np.load("../data/npyData/E123-H3K79me2.exonDef_ss_100.npy")
        E123_H3K9ac = np.load("../data/npyData/E123-H3K9ac.exonDef_ss_100.npy")
        E123_H3K9me1 = np.load("../data/npyData/E123-H3K9me1.exonDef_ss_100.npy")
        E123_H3K9me3 = np.load("../data/npyData/E123-H3K9me3.exonDef_ss_100.npy")
        E123_H4K20me1 = np.load("../data/npyData/E123-H4K20me1.exonDef_ss_100.npy")
        E123_Methylation = np.load("../data/npyData/E123-Methylation.exonDef_ss_100.npy")
        E123_Nucleosome = np.load("../data/npyData/E123-Nucleosome.exonDef_ss_100.npy")
        E123_CORE = np.concatenate((E123_H3K4me1,E123_H3K4me3,E123_H3K27me3,E123_H3K36me3,E123_H3K9me3),axis=2)
        E123_EXTRA = np.concatenate((E123_H3K9ac,E123_H3K27ac,E123_H3K4me2,E123_H3K79me2,E123_H4K20me1,E123_H2A,E123_H3K9me1,E123_DNase,E123_Methylation,E123_Nucleosome),axis=2)
        inputX_SHORT = np.concatenate((E123_DNA,E123_CORE),axis=2)
        inputX_LONG = np.concatenate((E123_DNA,E123_CORE,E123_EXTRA),axis=2)

    else:
        print 'Error:',EID,'Not Found'
        sys.exit(1)

    print "Input X (Core):",inputX_SHORT.shape
    print "Sample X (Core):",inputX_SHORT[0,:,:]

    print "Input X (Full):",inputX_LONG.shape
    print "Sample X (Full):",inputX_LONG[0,:,:]

    print "Input Y:",inputY.shape
    print "Sample Y:",inputY[0,:]

    print 'Done'

    return inputX_SHORT,inputX_LONG,inputY

def loadData(EID, SPAN):

    print 'Loading Data..'
    print 'EID:',EID
    print 'SPAN:',SPAN

    if EID == "E027":

        E027_DNA = np.load("../data/npyData/E027-DNA.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E027-EXP.exonDef_ss_"+SPAN+".npy")
        E027_H3K27me3 = np.load("../data/npyData/E027-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E027_H3K36me3 = np.load("../data/npyData/E027-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E027_H3K4me1 = np.load("../data/npyData/E027-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E027_H3K4me3 = np.load("../data/npyData/E027-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E027_H3K9ac = np.load("../data/npyData/E027-H3K9ac.exonDef_ss_"+SPAN+".npy")
        E027_H3K9me3 = np.load("../data/npyData/E027-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E027_Methylation = np.load("../data/npyData/E027-Methylation.exonDef_ss_"+SPAN+".npy")
        E027_CORE = np.concatenate((E027_H3K4me1,E027_H3K4me3,E027_H3K27me3,E027_H3K36me3,E027_H3K9me3),axis=2)
        E027_EXTRA = np.concatenate((E027_H3K9ac,E027_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E027_DNA,E027_CORE),axis=2)
        inputX_LONG = np.concatenate((E027_DNA,E027_CORE,E027_EXTRA),axis=2)

    elif EID == "E028":

        E028_DNA = np.load("../data/npyData/E028-DNA.exonDef_ss_"+SPAN+".npy")
        E028_DNase = np.load("../data/npyData/E028-DNase.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E028-EXP.exonDef_ss_"+SPAN+".npy")
        E028_H3K27me3 = np.load("../data/npyData/E028-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E028_H3K36me3 = np.load("../data/npyData/E028-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E028_H3K4me1 = np.load("../data/npyData/E028-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E028_H3K4me3 = np.load("../data/npyData/E028-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E028_H3K9me3 = np.load("../data/npyData/E028-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E028_Methylation = np.load("../data/npyData/E028-Methylation.exonDef_ss_"+SPAN+".npy")
        E028_CORE = np.concatenate((E028_H3K4me1,E028_H3K4me3,E028_H3K27me3,E028_H3K36me3,E028_H3K9me3),axis=2)
        E028_EXTRA = np.concatenate((E028_DNase,E028_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E028_DNA,E028_CORE),axis=2)
        inputX_LONG = np.concatenate((E028_DNA,E028_CORE,E028_EXTRA),axis=2)

    elif EID == "E066":

        E066_DNA = np.load("../data/npyData/E066-DNA.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E066-EXP.exonDef_ss_"+SPAN+".npy")
        E066_H3K27ac = np.load("../data/npyData/E066-H3K27ac.exonDef_ss_"+SPAN+".npy")
        E066_H3K27me3 = np.load("../data/npyData/E066-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E066_H3K36me3 = np.load("../data/npyData/E066-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E066_H3K4me1 = np.load("../data/npyData/E066-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E066_H3K4me3 = np.load("../data/npyData/E066-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E066_H3K9ac = np.load("../data/npyData/E066-H3K9ac.exonDef_ss_"+SPAN+".npy")
        E066_H3K9me3 = np.load("../data/npyData/E066-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E066_Methylation = np.load("../data/npyData/E066-Methylation.exonDef_ss_"+SPAN+".npy")
        E066_CORE = np.concatenate((E066_H3K4me1,E066_H3K4me3,E066_H3K27me3,E066_H3K36me3,E066_H3K9me3),axis=2)
        E066_EXTRA = np.concatenate((E066_H3K9ac,E066_H3K27ac,E066_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E066_DNA,E066_CORE),axis=2)
        inputX_LONG = np.concatenate((E066_DNA,E066_CORE,E066_EXTRA),axis=2)

    elif EID == "E096":

        E096_DNA = np.load("../data/npyData/E096-DNA.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E096-EXP.exonDef_ss_"+SPAN+".npy")
        E096_H3K27ac = np.load("../data/npyData/E096-H3K27ac.exonDef_ss_"+SPAN+".npy")
        E096_H3K27me3 = np.load("../data/npyData/E096-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E096_H3K36me3 = np.load("../data/npyData/E096-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E096_H3K4me1 = np.load("../data/npyData/E096-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E096_H3K4me3 = np.load("../data/npyData/E096-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E096_H3K9me3 = np.load("../data/npyData/E096-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E096_Methylation = np.load("../data/npyData/E096-Methylation.exonDef_ss_"+SPAN+".npy")
        E096_CORE = np.concatenate((E096_H3K4me1,E096_H3K4me3,E096_H3K27me3,E096_H3K36me3,E096_H3K9me3),axis=2)
        E096_EXTRA = np.concatenate((E096_H3K27ac,E096_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E096_DNA,E096_CORE),axis=2)
        inputX_LONG = np.concatenate((E096_DNA,E096_CORE,E096_EXTRA),axis=2)

    elif EID == "E114":

        E114_DNA = np.load("../data/npyData/E114-DNA.exonDef_ss_"+SPAN+".npy")
        E114_DNase = np.load("../data/npyData/E114-DNase.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E114-EXP.exonDef_ss_"+SPAN+".npy")
        E114_H2A = np.load("../data/npyData/E114-H2A.Z.exonDef_ss_"+SPAN+".npy")
        E114_H3K27ac = np.load("../data/npyData/E114-H3K27ac.exonDef_ss_"+SPAN+".npy")
        E114_H3K27me3 = np.load("../data/npyData/E114-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E114_H3K36me3 = np.load("../data/npyData/E114-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E114_H3K4me1 = np.load("../data/npyData/E114-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E114_H3K4me2 = np.load("../data/npyData/E114-H3K4me2.exonDef_ss_"+SPAN+".npy")
        E114_H3K4me3 = np.load("../data/npyData/E114-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E114_H3K79me2 = np.load("../data/npyData/E114-H3K79me2.exonDef_ss_"+SPAN+".npy")
        E114_H3K9ac = np.load("../data/npyData/E114-H3K9ac.exonDef_ss_"+SPAN+".npy")
        E114_H3K9me3 = np.load("../data/npyData/E114-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E114_H4K20me1 = np.load("../data/npyData/E114-H4K20me1.exonDef_ss_"+SPAN+".npy")
        E114_Methylation = np.load("../data/npyData/E114-Methylation.exonDef_ss_"+SPAN+".npy")
        E114_CORE = np.concatenate((E114_H3K4me1,E114_H3K4me3,E114_H3K27me3,E114_H3K36me3,E114_H3K9me3),axis=2)
        E114_EXTRA = np.concatenate((E114_H3K9ac,E114_H3K27ac,E114_H3K4me2,E114_H3K79me2,E114_H4K20me1,E114_H2A,E114_DNase,E114_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E114_DNA,E114_CORE),axis=2)
        inputX_LONG = np.concatenate((E114_DNA,E114_CORE,E114_EXTRA),axis=2)

    elif EID == "E116":

        E116_DNA = np.load("../data/npyData/E116-DNA.exonDef_ss_"+SPAN+".npy")
        E116_DNase = np.load("../data/npyData/E116-DNase.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E116-EXP.exonDef_ss_"+SPAN+".npy")
        E116_H2A = np.load("../data/npyData/E116-H2A.Z.exonDef_ss_"+SPAN+".npy")
        E116_H3K27ac = np.load("../data/npyData/E116-H3K27ac.exonDef_ss_"+SPAN+".npy")
        E116_H3K27me3 = np.load("../data/npyData/E116-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E116_H3K36me3 = np.load("../data/npyData/E116-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E116_H3K4me1 = np.load("../data/npyData/E116-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E116_H3K4me2 = np.load("../data/npyData/E116-H3K4me2.exonDef_ss_"+SPAN+".npy")
        E116_H3K4me3 = np.load("../data/npyData/E116-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E116_H3K79me2 = np.load("../data/npyData/E116-H3K79me2.exonDef_ss_"+SPAN+".npy")
        E116_H3K9ac = np.load("../data/npyData/E116-H3K9ac.exonDef_ss_"+SPAN+".npy")
        E116_H3K9me3 = np.load("../data/npyData/E116-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E116_H4K20me1 = np.load("../data/npyData/E116-H4K20me1.exonDef_ss_"+SPAN+".npy")
        E116_Methylation = np.load("../data/npyData/E116-Methylation.exonDef_ss_"+SPAN+".npy")
        E116_Nucleosome = np.load("../data/npyData/E116-Nucleosome.exonDef_ss_"+SPAN+".npy")
        E116_CORE = np.concatenate((E116_H3K4me1,E116_H3K4me3,E116_H3K27me3,E116_H3K36me3,E116_H3K9me3),axis=2)
        E116_EXTRA = np.concatenate((E116_H3K9ac,E116_H3K27ac,E116_H3K4me2,E116_H3K79me2,E116_H4K20me1,E116_H2A,E116_DNase,E116_Methylation,E116_Nucleosome),axis=2)
        inputX_SHORT = np.concatenate((E116_DNA,E116_CORE),axis=2)
        inputX_LONG = np.concatenate((E116_DNA,E116_CORE,E116_EXTRA),axis=2)

    elif EID == "E118":

        E118_DNA = np.load("../data/npyData/E118-DNA.exonDef_ss_"+SPAN+".npy")
        E118_DNase = np.load("../data/npyData/E118-DNase.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E118-EXP.exonDef_ss_"+SPAN+".npy")
        E118_H2A = np.load("../data/npyData/E118-H2A.Z.exonDef_ss_"+SPAN+".npy")
        E118_H3K27ac = np.load("../data/npyData/E118-H3K27ac.exonDef_ss_"+SPAN+".npy")
        E118_H3K27me3 = np.load("../data/npyData/E118-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E118_H3K36me3 = np.load("../data/npyData/E118-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E118_H3K4me1 = np.load("../data/npyData/E118-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E118_H3K4me2 = np.load("../data/npyData/E118-H3K4me2.exonDef_ss_"+SPAN+".npy")
        E118_H3K4me3 = np.load("../data/npyData/E118-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E118_H3K79me2 = np.load("../data/npyData/E118-H3K79me2.exonDef_ss_"+SPAN+".npy")
        E118_H3K9ac = np.load("../data/npyData/E118-H3K9ac.exonDef_ss_"+SPAN+".npy")
        E118_H3K9me3 = np.load("../data/npyData/E118-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E118_H4K20me1 = np.load("../data/npyData/E118-H4K20me1.exonDef_ss_"+SPAN+".npy")
        E118_Methylation = np.load("../data/npyData/E118-Methylation.exonDef_ss_"+SPAN+".npy")
        E118_CORE = np.concatenate((E118_H3K4me1,E118_H3K4me3,E118_H3K27me3,E118_H3K36me3,E118_H3K9me3),axis=2)
        E118_EXTRA = np.concatenate((E118_H3K9ac,E118_H3K27ac,E118_H3K4me2,E118_H3K79me2,E118_H4K20me1,E118_H2A,E118_DNase,E118_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E118_DNA,E118_CORE),axis=2)
        inputX_LONG = np.concatenate((E118_DNA,E118_CORE,E118_EXTRA),axis=2)

    elif EID == "E119":

        E119_DNA = np.load("../data/npyData/E119-DNA.exonDef_ss_"+SPAN+".npy")
        E119_DNase = np.load("../data/npyData/E119-DNase.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E119-EXP.exonDef_ss_"+SPAN+".npy")
        E119_H2A = np.load("../data/npyData/E119-H2A.Z.exonDef_ss_"+SPAN+".npy")
        E119_H3K27ac = np.load("../data/npyData/E119-H3K27ac.exonDef_ss_"+SPAN+".npy")
        E119_H3K27me3 = np.load("../data/npyData/E119-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E119_H3K36me3 = np.load("../data/npyData/E119-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E119_H3K4me1 = np.load("../data/npyData/E119-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E119_H3K4me2 = np.load("../data/npyData/E119-H3K4me2.exonDef_ss_"+SPAN+".npy")
        E119_H3K4me3 = np.load("../data/npyData/E119-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E119_H3K79me2 = np.load("../data/npyData/E119-H3K79me2.exonDef_ss_"+SPAN+".npy")
        E119_H3K9ac = np.load("../data/npyData/E119-H3K9ac.exonDef_ss_"+SPAN+".npy")
        E119_H3K9me3 = np.load("../data/npyData/E119-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E119_H4K20me1 = np.load("../data/npyData/E119-H4K20me1.exonDef_ss_"+SPAN+".npy")
        E119_Methylation = np.load("../data/npyData/E119-Methylation.exonDef_ss_"+SPAN+".npy")
        E119_CORE = np.concatenate((E119_H3K4me1,E119_H3K4me3,E119_H3K27me3,E119_H3K36me3,E119_H3K9me3),axis=2)
        E119_EXTRA = np.concatenate((E119_H3K9ac,E119_H3K27ac,E119_H3K4me2,E119_H3K79me2,E119_H4K20me1,E119_H2A,E119_DNase,E119_Methylation),axis=2)
        inputX_SHORT = np.concatenate((E119_DNA,E119_CORE),axis=2)
        inputX_LONG = np.concatenate((E119_DNA,E119_CORE,E119_EXTRA),axis=2)

    elif EID == "E123":

        E123_DNA = np.load("../data/npyData/E123-DNA.exonDef_ss_"+SPAN+".npy")
        E123_DNase = np.load("../data/npyData/E123-DNase.exonDef_ss_"+SPAN+".npy")
        inputY = np.load("../data/npyData/E123-EXP.exonDef_ss_"+SPAN+".npy")
        E123_H2A = np.load("../data/npyData/E123-H2A.Z.exonDef_ss_"+SPAN+".npy")
        E123_H3K27ac = np.load("../data/npyData/E123-H3K27ac.exonDef_ss_"+SPAN+".npy")
        E123_H3K27me3 = np.load("../data/npyData/E123-H3K27me3.exonDef_ss_"+SPAN+".npy")
        E123_H3K36me3 = np.load("../data/npyData/E123-H3K36me3.exonDef_ss_"+SPAN+".npy")
        E123_H3K4me1 = np.load("../data/npyData/E123-H3K4me1.exonDef_ss_"+SPAN+".npy")
        E123_H3K4me2 = np.load("../data/npyData/E123-H3K4me2.exonDef_ss_"+SPAN+".npy")
        E123_H3K4me3 = np.load("../data/npyData/E123-H3K4me3.exonDef_ss_"+SPAN+".npy")
        E123_H3K79me2 = np.load("../data/npyData/E123-H3K79me2.exonDef_ss_"+SPAN+".npy")
        E123_H3K9ac = np.load("../data/npyData/E123-H3K9ac.exonDef_ss_"+SPAN+".npy")
        E123_H3K9me1 = np.load("../data/npyData/E123-H3K9me1.exonDef_ss_"+SPAN+".npy")
        E123_H3K9me3 = np.load("../data/npyData/E123-H3K9me3.exonDef_ss_"+SPAN+".npy")
        E123_H4K20me1 = np.load("../data/npyData/E123-H4K20me1.exonDef_ss_"+SPAN+".npy")
        E123_Methylation = np.load("../data/npyData/E123-Methylation.exonDef_ss_"+SPAN+".npy")
        E123_Nucleosome = np.load("../data/npyData/E123-Nucleosome.exonDef_ss_"+SPAN+".npy")
        E123_CORE = np.concatenate((E123_H3K4me1,E123_H3K4me3,E123_H3K27me3,E123_H3K36me3,E123_H3K9me3),axis=2)
        E123_EXTRA = np.concatenate((E123_H3K9ac,E123_H3K27ac,E123_H3K4me2,E123_H3K79me2,E123_H4K20me1,E123_H2A,E123_H3K9me1,E123_DNase,E123_Methylation,E123_Nucleosome),axis=2)
        inputX_SHORT = np.concatenate((E123_DNA,E123_CORE),axis=2)
        inputX_LONG = np.concatenate((E123_DNA,E123_CORE,E123_EXTRA),axis=2)

    else:
        print 'Error:',EID,'Not Found'
        sys.exit(1)

    print "Input X (Core):",inputX_SHORT.shape
    print "Sample X (Core):",inputX_SHORT[0,:,:]

    print "Input X (Full):",inputX_LONG.shape
    print "Sample X (Full):",inputX_LONG[0,:,:]

    print "Input Y:",inputY.shape
    print "Sample Y:",inputY[0,:]

    print 'Done'

    return inputX_SHORT,inputX_LONG,inputY