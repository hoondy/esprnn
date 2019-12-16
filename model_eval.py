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

from sklearn.metrics import roc_auc_score, f1_score, roc_curve, auc, accuracy_score, r2_score
from sklearn.metrics import average_precision_score, precision_recall_curve

def predModel(model, inputX, BATCH_SIZE=100, VERBOSE=1):

    return model.predict(inputX, batch_size=BATCH_SIZE, verbose=VERBOSE)

def calc_accuracy_score(Y_true, Y_pred, threshold=0.5):

    Y_true = Y_true[:,-1]
    Y_pred = np.array(Y_pred[:,-1]>threshold).astype(int)

    return accuracy_score(Y_true, Y_pred)

def calc_f1_score(Y_true, Y_pred, threshold=0.5):

    Y_true = Y_true[:,-1]
    predY = np.array(Y_pred[:,-1]>threshold).astype(int)

    return f1_score(Y_true, predY)

def calc_roc_auc_score(Y_true, Y_pred):

    Y_true = Y_true[:,-1]
    Y_pred = Y_pred[:,-1]

    return roc_auc_score(Y_true, Y_pred)

def plot_roc(trueY, predY, PREFIX):

    # Compute ROC curve and ROC area
    fpr, tpr, _ = roc_curve(trueY[:,-1], predY[:,-1])
    roc_auc = auc(fpr, tpr)

    # Plot of a ROC curve for a specific class
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve of '+PREFIX)
    plt.legend(loc="lower right")
    plt.savefig(PREFIX+'_ROC.pdf',format='pdf')

    print('File',PREFIX+"_ROC.pdf","Saved")

def plot_loss(history, PREFIX):

    plt.title('Loss')
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Test')
    plt.legend()
    plt.savefig(PREFIX+"_loss.pdf")
    print("File",PREFIX+"_loss.pdf","Saved")

    plt.title('Accuracy')
    plt.plot(history.history['acc'], label='Train')
    plt.plot(history.history['val_acc'], label='Test')
    plt.legend()
    plt.savefig(PREFIX+"_acc.pdf")
    print("File",PREFIX+"_acc.pdf","Saved")

def calc_r2_score(Y_true, Y_pred):
    return r2_score(Y_true, Y_pred)

def plot_pr(Y_true, Y_pred, PREFIX):

    lines = []
    labels = []

    # calculate precision-recall curve
    precision, recall, thresholds = precision_recall_curve(Y_true, Y_pred)

    # calculate precision-recall metric
    f1, auprc, avg_precision= f1_score(Y_true, Y_pred), auc(precision, recall), average_precision_score(Y_true, Y_pred)

    l, = plt.step(precision, recall, color='navy', alpha=0.5, where='post', lw=3)
    lines.append(l)
    labels.append('F1={0:0.2f} AUC={0:0.2f} Avg={0:0.2f}'.format(f1,auprc,avg_precision))

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('{0} Precision-Recall curve'.format(PREFIX))
    plt.legend(lines, labels, loc=(0.1, 0.1), prop=dict(size=14))
    plt.savefig(PREFIX+"_PR.pdf", bbox_inches='tight')
