#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2019"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, sys
from keras import layers
from keras import models
import model_eval, model_io
import numpy as np
from sklearn.model_selection import train_test_split
import h5py

### Usage: python model_train.py -n TEST -m LSTM -s 100 -p "/path/to/npyData" -e 50
### -x E123-DNA.exonDef_ss_100.npy,E123-DNase.exonDef_ss_100.npy,E123-H3K27me3.exonDef_ss_100.npy,E123-H3K4me3.exonDef_ss_100.npy
### -y E123-EXP.exonDef_ss_100.npy

parser = argparse.ArgumentParser(description='Train Model')

parser.add_argument('-p','--prefix', help='prefix for output files',required=True)
parser.add_argument('-x','--input', help='input HDF5 data',required=True)

parser.add_argument('-m','--model', help='RNN model: LSTM,GRU,RNN',required=False, default="LSTM")
parser.add_argument('-s','--span', help='span size from splice site',required=False, type=int, default=200)
parser.add_argument('-e','--epoch', help='epoch',required=False, type=int, default=20)
parser.add_argument('-d','--dropout', help='dropout',required=False, type=float, default=0.3)
parser.add_argument('-b','--batchsize', help='batch size',required=False, type=int, default=100)
parser.add_argument('-r','--randomstate', help='random state',required=False, type=int, default=38)
parser.add_argument('-t','--testsize', help='test size fraction',required=False, type=float, default=0.2)
parser.add_argument('-v','--verbose', help='test size fraction',required=False, type=int, default=1) # verbose: 0 for no logging to stdout, 1 for progress bar logging, 2 for one log line per epoch.

args = parser.parse_args()

### PARAMETERS ###

PREFIX = args.prefix
MODEL = args.model
SPAN = args.span
EPOCHS = args.epoch
DROPOUT = args.dropout
BATCH_SIZE = args.batchsize
RANDOM_STATE = args.randomstate
TEST_SIZE = args.testsize
VERBOSE = args.verbose

print("PREFIX:",PREFIX)
print("MODEL:",MODEL)
print("SPAN:",str(SPAN))
print("EPOCHS:",str(EPOCHS))
print("DROPOUT:",str(DROPOUT))
print("BATCH_SIZE:",str(BATCH_SIZE))
print("RANDOM_STATE:",str(RANDOM_STATE))
print("TEST_SIZE:",str(TEST_SIZE))
print("VERBOSE:",str(VERBOSE))

### TRAIN TEST SPLIT ###
'''
Terminology defined

Training data (64% of original data): data used to train the model
Validation data (16% of original data): data used for evaluating model fit during training
Test data (20% of original data): data used for evaluating the final model fit

By default, data is first split 8:2 train and test. 80% of training data is then split again between 8:2 (64% and 16% of original) train:validation during training phase
'''
print("Splitting data into train and test set")
with h5py.File(args.input, 'r') as f:
    X_train, X_test, Y_train, Y_test = train_test_split(np.array(f['x']), np.array(f['y']), test_size=TEST_SIZE, random_state=RANDOM_STATE)

print("Train set size:",len(X_train))
print("Test set size:",len(X_test))

### BUILD MODEL ###

intron_exon_input = layers.Input(shape=(2*SPAN, X_train.shape[2]), name="intron_exon_3acc")
exon_intron_input = layers.Input(shape=(2*SPAN, X_train.shape[2]), name="exon_intron_5don")

if MODEL=="LSTM":
    print('Building LSTM model...')
    intron_exon_rnn = layers.LSTM(X_train.shape[2], return_sequences=True)(intron_exon_input)
    exon_intron_rnn = layers.LSTM(X_train.shape[2], return_sequences=True)(exon_intron_input)
    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.LSTM(X_train.shape[2], return_sequences=False)(merged)

elif MODEL=="GRU":
    print('Building GRU model...')
    intron_exon_rnn = layers.GRU(X_train.shape[2], return_sequences=True)(intron_exon_input)
    exon_intron_rnn = layers.GRU(X_train.shape[2], return_sequences=True)(exon_intron_input)
    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.GRU(X_train.shape[2], return_sequences=False)(merged)

elif MODEL=="RNN":
    print('Building SimpleRNN model...')
    intron_exon_rnn = layers.SimpleRNN(X_train.shape[2], return_sequences=True)(intron_exon_input)
    exon_intron_rnn = layers.SimpleRNN(X_train.shape[2], return_sequences=True)(exon_intron_input)
    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.SimpleRNN(X_train.shape[2], return_sequences=False)(merged)

else:
    print('-m or --model parameter not recognized...')
    sys.exit(1)

merged_dropout = layers.Dropout(DROPOUT)(merged_rnn)
merged_output = layers.Dense(1, activation='sigmoid')(merged_dropout)
model = models.Model(inputs=[intron_exon_input, exon_intron_input], outputs=merged_output)
model.compile(loss='mean_squared_error',optimizer='adam',metrics=['mean_squared_error','accuracy'])
model.summary()

### TRAIN ###

print('Train...')
model.fit([X_train[:100000,:2*SPAN,:], X_train[:100000,2*SPAN:,:]], Y_train, epochs=EPOCHS, validation_split=TEST_SIZE, batch_size=BATCH_SIZE, verbose=1)

### SAVE DATA ###

model_io.saveModel(PREFIX, model)

### EVALUATE ###

loss, acc = model.evaluate([X_test[:,:2*SPAN,:], X_test[:,2*SPAN:,:]], Y_test, batch_size=BATCH_SIZE, verbose=VERBOSE)
print('Test Loss:', loss)
print('Test Accuracy:', acc)

### PREDICT ###

predY = model.predict([X_test[:,:2*SPAN,:], X_test[:,2*SPAN:,:]], batch_size=BATCH_SIZE, verbose=VERBOSE)
model_eval.save2npy(PREFIX+"_predY.npy",predY)

### ROC AUC ###

print('Test ROC AUC:', model_eval.calc_roc_auc_score(Y_test, predY))

### F1 SCORE ###

print('Test F1 Score:', model_eval.calc_f1_score(Y_test, predY))

### PLOT ROC AUC ###

model_eval.plot_roc_auc(Y_test, predY, PREFIX)