#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2016"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, sys
from keras import layers
from keras import models
import model_eval
import numpy as np

### Usage: python model_train.py -n TEST -m LSTM -s 100 -p "/path/to/npyData"
### -x E123-DNA.exonDef_ss_100.npy,E123-DNase.exonDef_ss_100.npy,E123-H3K27me3.exonDef_ss_100.npy,E123-H3K4me3.exonDef_ss_100.npy
### -y E123-EXP.exonDef_ss_100.npy

parser = argparse.ArgumentParser(description='Train Model')

parser.add_argument('-n','--name', help='model name',required=True)
parser.add_argument('-m','--model', help='RNN model: LSTM,GRU,SimpleRNN',required=True)

parser.add_argument('-s','--span', help='span size from splice site',required=True)
parser.add_argument('-p','--path', help='path to npy data',required=True)

parser.add_argument('-x','--input', help='input npy list, comma-seperated',required=True)
parser.add_argument('-y','--output', help='output npy',required=True)

args = parser.parse_args()

###

HIDDEN_SIZE = 4*int(args.span)
DROPOUT = 0.3
BATCH_SIZE = 100
EPOCHS = 50
MODEL_NAME = args.name

### LOAD DATA ###

print args.input

inputFiles = args.input.split(",")
print len(inputFiles)

for idx, file in enumerate(inputFiles):
    print "Loading ",file

    if idx==0:
        inputX=np.load(args.path+"/"+file)
    else:
        inputX=np.append(inputX, np.load(args.path+"/"+file), axis=2)

inputY = np.load(args.path+"/"+args.output)

### SPLIT DATA ###

input_3acc = inputX[:,0:inputX.shape[1]/2,:]
input_5don = inputX[:,inputX.shape[1]/2:inputX.shape[1],:]

print "3'ss X:",input_3acc.shape
print "5'ss X:",input_5don.shape

### BUILD MODEL ###

if args.model=="LSTM":

    print('Building LSTM model...')

    intron_exon_input = layers.Input(shape=(input_3acc.shape[1], input_3acc.shape[2]), name="intron_exon_3acc")
    intron_exon_rnn = layers.LSTM(HIDDEN_SIZE/2, return_sequences=True)(intron_exon_input)

    exon_intron_input = layers.Input(shape=(input_5don.shape[1], input_5don.shape[2]), name="exon_intron_5don")
    exon_intron_rnn = layers.LSTM(HIDDEN_SIZE/2, return_sequences=True)(exon_intron_input)

    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.LSTM(HIDDEN_SIZE, return_sequences=False)(merged)
    merged_dropout = layers.Dropout(DROPOUT)(merged_rnn)
    merged_output = layers.Dense(inputY.shape[1], activation='softmax')(merged_dropout)

    model = models.Model(inputs=[intron_exon_input, exon_intron_input], outputs=merged_output)
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.summary()

elif args.model=="GRU":

    print('Building GRU model...')

    intron_exon_input = layers.Input(shape=(input_3acc.shape[1], input_3acc.shape[2]), name="intron_exon_3acc")
    intron_exon_rnn = layers.GRU(HIDDEN_SIZE/2, return_sequences=True)(intron_exon_input)

    exon_intron_input = layers.Input(shape=(input_5don.shape[1], input_5don.shape[2]), name="exon_intron_5don")
    exon_intron_rnn = layers.GRU(HIDDEN_SIZE/2, return_sequences=True)(exon_intron_input)

    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.GRU(HIDDEN_SIZE, return_sequences=False)(merged)
    merged_dropout = layers.Dropout(DROPOUT)(merged_rnn)
    merged_output = layers.Dense(inputY.shape[1], activation='softmax')(merged_dropout)

    model = models.Model(inputs=[intron_exon_input, exon_intron_input], outputs=merged_output)
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.summary()

elif args.model=="SimpleRNN":

    print('Building SimpleRNN model...')

    intron_exon_input = layers.Input(shape=(input_3acc.shape[1], input_3acc.shape[2]), name="intron_exon_3acc")
    intron_exon_rnn = layers.SimpleRNN(HIDDEN_SIZE/2, return_sequences=True)(intron_exon_input)

    exon_intron_input = layers.Input(shape=(input_5don.shape[1], input_5don.shape[2]), name="exon_intron_5don")
    exon_intron_rnn = layers.SimpleRNN(HIDDEN_SIZE/2, return_sequences=True)(exon_intron_input)

    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.SimpleRNN(HIDDEN_SIZE, return_sequences=False)(merged)
    merged_dropout = layers.Dropout(DROPOUT)(merged_rnn)
    merged_output = layers.Dense(inputY.shape[1], activation='softmax')(merged_dropout)

    model = models.Model(inputs=[intron_exon_input, exon_intron_input], outputs=merged_output)
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.summary()

else:
    print('-m or --model parameter not recognized...')
    sys.exit(1)

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
