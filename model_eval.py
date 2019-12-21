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

def calc_accuracy_score(Y_true, Y_pred):
    Y_true = Y_true[:,-1]
    Y_pred = Y_pred[:,-1]
    threshold=len(Y_true[Y_true==1]) / len(Y_true)
    Y_pred_binary = np.array(Y_pred>threshold).astype(int)
    return accuracy_score(Y_true, Y_pred_binary)

def calc_f1_score(Y_true, Y_pred):
    Y_true = Y_true[:,-1]
    Y_pred = Y_pred[:,-1]
    threshold=len(Y_true[Y_true==1]) / len(Y_true)
    Y_pred_binary = np.array(Y_pred>threshold).astype(int)
    return f1_score(Y_true, Y_pred_binary)

def calc_roc_auc_score(Y_true, Y_pred):
    Y_true = Y_true[:,-1]
    Y_pred = Y_pred[:,-1]
    return roc_auc_score(Y_true, Y_pred)

def plot_roc(Y_true, Y_pred, PREFIX):
    Y_true = Y_true[:,-1]
    Y_pred = Y_pred[:,-1]

    # Compute ROC curve and ROC area
    fpr, tpr, _ = roc_curve(Y_true, Y_pred)
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
    plt.clf()

def plot_loss(history, PREFIX):

    plt.title('Loss')
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Test')
    plt.legend()
    plt.savefig(PREFIX+"_loss.pdf")
    print("File",PREFIX+"_loss.pdf","Saved")
    plt.clf()

    plt.title('Accuracy')
    plt.plot(history.history['acc'], label='Train')
    plt.plot(history.history['val_acc'], label='Test')
    plt.legend()
    plt.savefig(PREFIX+"_acc.pdf")
    print("File",PREFIX+"_acc.pdf","Saved")
    plt.clf()

def calc_r2_score(Y_true, Y_pred):
    Y_true = Y_true[:,-1]
    Y_pred = Y_pred[:,-1]
    return r2_score(Y_true, Y_pred)

def plot_pr(Y_true, Y_pred, PREFIX):
    Y_true = Y_true[:,-1]
    Y_pred = Y_pred[:,-1]

    # calculate precision-recall curve
    precision, recall, _ = precision_recall_curve(Y_true, Y_pred)
    pr_auc = auc(recall, precision)
    pr_ap = average_precision_score(Y_true, Y_pred)

    # summarize scores
    print('Precision-Recall curve: auc=%.3f ap=%.3f' % (pr_auc,pr_ap))

    # plot the precision-recall curves
    plt.plot(recall, precision, marker='.', color='navy', alpha=0.5, lw=3)
    pr_rand = len(Y_true[Y_true==1]) / len(Y_true)
    plt.plot([0, 1], [pr_rand, pr_rand], linestyle='--', color='teal', alpha=0.5)

    # axis labels
    plt.xlabel('Recall')
    plt.ylabel('Precision')

    # axis limit
    plt.xlim([0.0, 1.0])

    # title
    plt.title('{0} Precision-Recall curve'.format(PREFIX))

    # show the legend
    plt.legend(['auc={0:0.2f} ap={0:0.2f}'.format(pr_auc,pr_ap),'random'])

    # save the plot
    plt.savefig(PREFIX+"_PR.pdf", bbox_inches='tight')
    plt.clf()
