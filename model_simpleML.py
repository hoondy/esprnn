#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2017"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, sys
import model_eval
import numpy as np
from sklearn import svm,tree,neighbors,ensemble
from sklearn.model_selection import train_test_split

### Usage: python model_simpleML.py -n TEST -m SVM -p "/path/to/npyData"
### -x E123-DNA.exonDef_ss_100.npy,E123-DNase.exonDef_ss_100.npy,E123-H3K27me3.exonDef_ss_100.npy,E123-H3K4me3.exonDef_ss_100.npy
### -y E123-EXP.exonDef_ss_100.npy

parser = argparse.ArgumentParser(description='Train Model')

parser.add_argument('-n','--name', help='model name',required=True)
parser.add_argument('-m','--model', help='ML model: SVM,TREE,KNN,RF',required=True)

parser.add_argument('-p','--path', help='path to npy data',required=True)
parser.add_argument('-x','--input', help='input npy list, comma-separated',required=True)
parser.add_argument('-y','--output', help='output npy',required=True)

args = parser.parse_args()

###

MODEL_NAME = args.name

### LOAD DATA ###

inputFiles = args.input.split(",")
print "Found",len(inputFiles),"files"

for idx, file in enumerate(inputFiles):
    print "Loading ",file

    if idx==0:
        inputX=np.load(args.path+"/"+file)
    else:
        inputX=np.append(inputX, np.load(args.path+"/"+file), axis=-1)

inputY = np.load(args.path+"/"+args.output)

### FLATTEN

inputX = inputX.reshape(len(inputX),-1)
print "Input reshaped to",inputX.shape

### TRAIN TEST SPLIT ###

print "Splitting data into train and test set"
X_train, X_test, Y_train, Y_test = train_test_split(inputX, inputY, test_size=0.1) #random_state=42 if needed
print "Train set size:",len(X_train)
print "Test set size:",len(X_test)

Y_train = Y_train[:,-1]
Y_test = Y_test[:,-1]

### Sub-sampling

# trainsize = 1000
# X_train = X_train[:trainsize]
# Y_train = Y_train[:trainsize]
#
# print X_train.shape
# print Y_train.shape

### CLASSIFICATION ###

if args.model=="SVM":
    classifier = svm.SVC(kernel='rbf')
elif args.model=="TREE":
    classifier = tree.DecisionTreeClassifier()
elif args.model=="KNN":
    classifier = neighbors.KNeighborsClassifier(n_neighbors=5)
elif args.model=="RF":
    classifier = ensemble.RandomForestClassifier(n_estimators=10)
else:
    print "Model not found: select one of SVM, TREE, KNN, or RF models"
    sys.exit(1)

classifier.fit(X_train, Y_train)

### EVALUATE ###

print 'Test Score:', classifier.score(X_test, Y_test)

### PREDICT ###

predY = classifier.predict_proba(X_test) # predict as probability
trueY = np.stack((Y_test==0,Y_test==1),axis=1).astype(int)

print 'Accuracy Score:', model_eval.calc_accuracy_score(trueY, predY)

### ROC AUC ###

print 'Test ROC AUC:', model_eval.calc_roc_auc_score(trueY, predY)

### F1 ###

print 'Test F1 Score:', model_eval.calc_f1_score(trueY, predY)

### PLOT ROC AUC ###

model_eval.plot_roc_auc(trueY, predY, "SimpleML_"+args.model)






