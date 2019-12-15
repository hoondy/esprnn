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

from sklearn.metrics import roc_auc_score, f1_score, roc_curve, auc, accuracy_score

def predModel(model, inputX):

    return model.predict(inputX, batch_size=100, verbose=1)

def calc_accuracy_score(trueY, predY, threshold=0.5):

    trueY = trueY[:,1]
    predY = np.array(predY[:,1]>threshold).astype(int)

    return accuracy_score(trueY, predY)

def calc_f1_score(trueY, predY, threshold=0.5):

    trueY = trueY[:,1]
    predY = np.array(predY[:,1]>threshold).astype(int)

    return f1_score(trueY, predY)

def calc_roc_auc_score(trueY, predY):

    trueY = trueY[:,1]
    predY = predY[:,1]

    return roc_auc_score(trueY, predY)

def plot_roc_auc(trueY, predY, MODEL_NAME):

    # Compute ROC curve and ROC area
    fpr, tpr, _ = roc_curve(trueY[:,1], predY[:,1])
    roc_auc = auc(fpr, tpr)

    # Plot of a ROC curve for a specific class
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve of '+MODEL_NAME)
    plt.legend(loc="lower right")
    plt.savefig(MODEL_NAME+'.pdf',format='pdf')

    print('Saved',MODEL_NAME+'.pdf')

def save2npy(fileName, var):
    np.save(fileName, var)
    print("File",fileName,"Saved")