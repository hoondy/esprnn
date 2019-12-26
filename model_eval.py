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

    # summarize scores
    print('ROC curve: AUC=%.3f' % (roc_auc))

    # Plot ROC curve
    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % roc_auc, color='navy', alpha=0.5, lw=3)
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)

    # axis limit
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])

    # axis labels
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    # title
    plt.title('ROC curve of '+PREFIX)

    # show the legend
    plt.legend(loc="lower right")

    # save the plot
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
    threshold=len(Y_true[Y_true==1]) / len(Y_true)
    Y_pred_binary = np.array(Y_pred>threshold).astype(int)
    pr_f1 = f1_score(Y_true, Y_pred_binary)

    # summarize scores
    print('Precision-Recall curve: AUC=%.3f AP=%.3f F1=%.3f' % (pr_auc,pr_ap,pr_f1))

    # plot the precision-recall curves
    plt.step(recall, precision, color='navy', alpha=0.5, where='post', lw=3)
    pr_rand = len(Y_true[Y_true==1]) / len(Y_true)
    plt.plot([0, 1], [pr_rand, pr_rand], linestyle='--', color='k', alpha=0.5)

    # axis labels
    plt.xlabel('Recall')
    plt.ylabel('Precision')

    # axis limit
    plt.xlim([0.0, 1.0])

    # title
    plt.title('PR curve of {0}'.format(PREFIX))

    # show the legend
    plt.legend(['PR curve (AUC=%.2f F1=%.2f)' % (pr_auc,pr_f1),'random'],loc="lower right")

    # save the plot
    plt.savefig(PREFIX+"_PR.pdf", bbox_inches='tight')
    print("File",PREFIX+"_PR.pdf","Saved")
    plt.clf()
