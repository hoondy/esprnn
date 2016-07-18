#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

###
### Predict Y and save results as NPY
###
### Usage: python postproc_modelPred.py -m splicing_model_lstm1 -e E028 --core
###

import argparse
import preproc_loadData
import model_eval

parser = argparse.ArgumentParser(description='Evaluate Model')
parser.add_argument('-m','--model', help='model name',required=True)
parser.add_argument('-e','--eid', help='sample eid',required=True)

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('--full', dest='feature', action='store_true')
group.add_argument('--core', dest='feature', action='store_false')
group.set_defaults(feature=True)

args = parser.parse_args()

###

MODEL_NAME = args.model
EID = args.eid

### LOAD DATA ###

if args.feature:
    print "Loading Full Dataset"
    MODEL_NAME = MODEL_NAME+"_"+EID+"_full"
    _, inputX, inputY = preproc_loadData.loadData(EID)
else:
    print "Loading Core Dataset"
    MODEL_NAME = MODEL_NAME+"_"+EID+"_core"
    inputX, _, inputY = preproc_loadData.loadData(EID)

### LOAD MODEL ###

model = model_eval.loadModel(MODEL_NAME)

### PREDICT ###

inputX_3acc = inputX[:,0:inputX.shape[1]/2,:]
inputX_5don = inputX[:,inputX.shape[1]/2:inputX.shape[1],:]

predY = model_eval.predModel(model, [inputX_3acc, inputX_5don])

model_eval.save2npy(MODEL_NAME+"_predY.npy",predY)

### ROC AUC ###

roc_auc = model_eval.calcROC_AUC(inputY, predY)
print 'Test ROC AUC:', roc_auc

### F1 ###

f1 = model_eval.calcF1(inputY, predY)
print 'Test F1 Score:', f1