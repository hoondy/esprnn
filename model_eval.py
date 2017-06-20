#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.metrics import roc_auc_score, f1_score, roc_curve, auc
from sklearn.preprocessing import label_binarize

def predModel(model, inputX):

    return model.predict(inputX, batch_size=100, verbose=1)

def calcROC_AUC(inputY, predY):

    roc_auc = roc_auc_score(inputY, predY)
    return roc_auc

def calcF1(inputY, predY):

    if len(inputY.shape)>1 and len(predY.shape)>1:
        print inputY.shape, predY.shape
        y_true = inputY[:,1]==1
        y_pred = predY[:,1]>0.5
    else:
        y_true = inputY
        y_pred = predY>0.5

    f1 = f1_score(y_true, y_pred)

    return f1

def plotROC_AUC(inputY, predY, MODEL_NAME):

    ##############################################################################
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    inputY = label_binarize(inputY, classes=[0, 1])
    predY = label_binarize(predY, classes=[0, 1])

    n_classes = inputY.shape[1]

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(inputY[:, i], predY[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    ##############################################################################
    # Plot of a ROC curve for a specific class
    plt.figure()
    plt.plot(fpr[n_classes-1], tpr[n_classes-1], label='ROC curve (area = %0.2f)' % roc_auc[n_classes-1])
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve')
    plt.legend(loc="lower right")
    plt.savefig(MODEL_NAME+'.png')

    print 'Saved',MODEL_NAME+'.png'

def save2npy(fileName, var):
    np.save(fileName, var)
    print "File",fileName,"Saved"