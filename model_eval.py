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
    plt.savefig(PREFIX+'_ROC.pdf', bbox_inches='tight')
    print('File',PREFIX+"_ROC.pdf","Saved")
    plt.clf()

def plot_loss(history, PREFIX):

    plt.title('Loss')
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Test')
    plt.legend()
    plt.savefig(PREFIX+"_loss.pdf", bbox_inches='tight')
    print("File",PREFIX+"_loss.pdf","Saved")
    plt.clf()

    plt.title('Accuracy')
    plt.plot(history.history['acc'], label='Train')
    plt.plot(history.history['val_acc'], label='Test')
    plt.legend()
    plt.savefig(PREFIX+"_acc.pdf", bbox_inches='tight')
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

def plot_roc_compare(Y_true1, Y_pred1, Y_true2, Y_pred2, label1, label2, PREFIX):
    Y_true1 = Y_true1[:,-1]
    Y_pred1 = Y_pred1[:,-1]
    Y_true2 = Y_true2[:,-1]
    Y_pred2 = Y_pred2[:,-1]

    # Compute ROC curve and ROC area
    fpr1, tpr1, _ = roc_curve(Y_true1, Y_pred1)
    roc_auc1 = auc(fpr1, tpr1)
    fpr2, tpr2, _ = roc_curve(Y_true2, Y_pred2)
    roc_auc2 = auc(fpr2, tpr2)

    # summarize scores
    print('ROC curve: AUC=%.3f' % (roc_auc1))
    print('ROC curve: AUC=%.3f' % (roc_auc2))

    # Plot ROC curve
    plt.figure()
    plt.plot(fpr1, tpr1, color='navy', alpha=0.5, lw=3)
    plt.plot(fpr2, tpr2, color='darkred', alpha=0.5, lw=3)
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
    plt.legend(['%s (AUC = %0.2f)' % (label1,roc_auc1),'%s (AUC = %0.2f)' % (label2,roc_auc2)], loc="lower right")

    # save the plot
    plt.savefig(PREFIX+'_ROC.pdf', bbox_inches='tight')
    print('File',PREFIX+"_ROC.pdf","Saved")
    plt.clf()

def plot_pr_compare(Y_true1, Y_pred1, Y_true2, Y_pred2, label1, label2, PREFIX):
    Y_true1 = Y_true1[:,-1]
    Y_pred1 = Y_pred1[:,-1]
    Y_true2 = Y_true2[:,-1]
    Y_pred2 = Y_pred2[:,-1]

    # calculate precision-recall curve
    precision1, recall1, _ = precision_recall_curve(Y_true1, Y_pred1)
    precision2, recall2, _ = precision_recall_curve(Y_true2, Y_pred2)

    pr_auc1 = auc(recall1, precision1)
    pr_ap1 = average_precision_score(Y_true1, Y_pred1)
    threshold1=len(Y_true1[Y_true1==1]) / len(Y_true1)
    Y_pred_binary1 = np.array(Y_pred1>threshold1).astype(int)
    pr_f11 = f1_score(Y_true1, Y_pred_binary1)

    pr_auc2 = auc(recall2, precision2)
    pr_ap2 = average_precision_score(Y_true2, Y_pred2)
    threshold2=len(Y_true2[Y_true2==1]) / len(Y_true2)
    Y_pred_binary2 = np.array(Y_pred2>threshold2).astype(int)
    pr_f12 = f1_score(Y_true2, Y_pred_binary2)

    # summarize scores
    print('Precision-Recall curve: AUC=%.3f AP=%.3f F1=%.3f' % (pr_auc1,pr_ap1,pr_f11))
    print('Precision-Recall curve: AUC=%.3f AP=%.3f F1=%.3f' % (pr_auc2,pr_ap2,pr_f12))

    # plot the precision-recall curves
    plt.step(recall1, precision1, color='navy', alpha=0.5, where='post', lw=3)
    plt.step(recall2, precision2, color='darkred', alpha=0.5, where='post', lw=3)

    # axis labels
    plt.xlabel('Recall')
    plt.ylabel('Precision')

    # axis limit
    plt.xlim([0.0, 1.0])

    # title
    plt.title('PR curve of {0}'.format(PREFIX))

    # show the legend
    plt.legend(['%s (AUC=%.2f F1=%.2f)' % (label1,pr_auc1,pr_f11),'%s (AUC=%.2f F1=%.2f)' % (label2,pr_auc2,pr_f12)],loc="lower right")

    # save the plot
    plt.savefig(PREFIX+"_PR.pdf", bbox_inches='tight')
    print("File",PREFIX+"_PR.pdf","Saved")
    plt.clf()