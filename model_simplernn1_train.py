#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse
from keras.models import Sequential
from keras.layers import Dense, Dropout, Merge
from keras.layers import LSTM, GRU, SimpleRNN
import preproc_loadData
import model_eval

### Usage: THEANO_FLAGS='floatX=float32,device=gpu,lib.cnmem=1' python model_simplernn1_train.py -e E123 --full

###

parser = argparse.ArgumentParser(description='Train Model')
parser.add_argument('-e','--eid', help='sample eid',required=True)

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('--full', dest='feature', action='store_true')
group.add_argument('--core', dest='feature', action='store_false')
group.set_defaults(feature=True)

args = parser.parse_args()

###

HIDDEN_SIZE = 400
DROPOUT = 0.3
BATCH_SIZE = 100
EPOCHS = 20
MODEL_NAME = 'splicing_model_simplernn1'
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

### SPLIT DATA ###

input_3acc = inputX[:,0:inputX.shape[1]/2,:]
input_5don = inputX[:,inputX.shape[1]/2:inputX.shape[1],:]

print "3'ss X:",input_3acc.shape
print "5'ss X:",input_5don.shape

### BUILD MODEL ###

print('Build model...')

intron_exon = Sequential()
intron_exon.add(SimpleRNN(HIDDEN_SIZE/2, return_sequences=True, input_shape=(input_3acc.shape[1], input_3acc.shape[2])))

exon_intron = Sequential()
exon_intron.add(SimpleRNN(HIDDEN_SIZE/2, return_sequences=True, input_shape=(input_5don.shape[1], input_5don.shape[2])))

model = Sequential()
model.add(Merge([intron_exon, exon_intron], mode='concat'))
model.add(SimpleRNN(HIDDEN_SIZE, return_sequences=False))
model.add(Dropout(DROPOUT))
model.add(Dense(inputY.shape[1], activation='softmax'))

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

model.summary()

### TRAIN ###

print('Train...')
model.fit([input_3acc, input_5don], inputY, epochs=EPOCHS, validation_split=0.05, batch_size=BATCH_SIZE, verbose=2)
# verbose: 0 for no logging to stdout, 1 for progress bar logging, 2 for one log line per epoch.

### SAVE DATA ###

open(MODEL_NAME+'.yaml', 'w').write(model.to_yaml())
model.save_weights(MODEL_NAME+'.h5')

### EVALUATE ###

score, acc = model.evaluate([input_3acc, input_5don], inputY, batch_size=BATCH_SIZE, verbose=2)
print('Test Score:', score)
print('Test Accuracy:', acc)

### PREDICT ###

predY = model_eval.predModel(model, [input_3acc, input_5don])
model_eval.save2npy(MODEL_NAME+"_predY.npy",predY)

### ROC AUC ###

roc_auc = model_eval.calcROC_AUC(inputY, predY)
print 'Test ROC AUC:', roc_auc

### F1 ###

f1 = model_eval.calcF1(inputY, predY)
print 'Test F1 Score:', f1

### PLOT ROC AUC ###

model_eval.plotROC_AUC(inputY, predY, MODEL_NAME)
