#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2019"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, sys
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import backend as K
from . import model_eval, model_io
import numpy as np
from sklearn.model_selection import train_test_split
import h5py

### Usage: python model_train.py --prefix K562_LSTM_200span --input K562_input.hdf5 --model LSTM --span 200

parser = argparse.ArgumentParser(description='Train RNN Model')

parser.add_argument('-p','--prefix', help='prefix for output files',required=True)
parser.add_argument('-x','--input', help='input HDF5 data',required=True)

parser.add_argument('-m','--model', help='RNN model: LSTM,GRU,RNN',required=False, default="LSTM")
parser.add_argument('-s','--span', help='span window size (input sequence length for each splice site)',required=False, type=int, default=400)
parser.add_argument('-e','--epoch', help='epoch',required=False, type=int, default=20)
parser.add_argument('-d','--dropout', help='dropout',required=False, type=float, default=0.3)
parser.add_argument('-b','--batchsize', help='batch size',required=False, type=int, default=100)
parser.add_argument('-r','--randomstate', help='random state',required=False, type=int, default=38)
parser.add_argument('-t','--testsize', help='test size fraction',required=False, type=float, default=0.2)
parser.add_argument('-v','--verbose', help='verbosity',required=False, type=int, default=1) # verbose: 0 for no logging to stdout, 1 for progress bar logging, 2 for one log line per epoch.
parser.add_argument('--hiddensize', help='hidden state size',required=False, type=int, default=2)

parser.add_argument('--activation', help='activation',required=False, default="sigmoid")
parser.add_argument('--optimizer', help='optimizer',required=False, default="adam")
args = parser.parse_args()

### PARAMETERS ###

param_PREFIX = args.prefix
param_MODEL = args.model
param_SPAN = args.span
param_DROPOUT = args.dropout
param_HIDDEN_STATE=args.hiddensize

param_EPOCHS = args.epoch
param_BATCH_SIZE = args.batchsize
param_RANDOM_STATE = args.randomstate
param_TEST_SIZE = args.testsize
param_VERBOSE = args.verbose

param_ACTIVATION = args.activation
param_OPTIMIZER = args.optimizer

print("PREFIX:",param_PREFIX)
print("MODEL:",param_MODEL)
print("SPAN:",str(param_SPAN))
print("DROPOUT:",str(param_DROPOUT))
print("HIDDEN_STATE:",str(param_HIDDEN_STATE))

print("EPOCHS:",str(param_EPOCHS))
print("BATCH_SIZE:",str(param_BATCH_SIZE))
print("RANDOM_STATE:",str(param_RANDOM_STATE))
print("TEST_SIZE:",str(param_TEST_SIZE))
print("VERBOSE:",str(param_VERBOSE))

print("ACTIVATION:",str(param_ACTIVATION))
print("OPTIMIZER:",str(param_OPTIMIZER))


### R2 metric for regression ###

def r2(y_true, y_pred):
    SS_res=K.sum(K.square(y_true-y_pred ))
    SS_tot=K.sum(K.square(y_true-K.mean(y_true)))
    return (1-SS_res/(SS_tot + K.epsilon())) # K.epsilon() is 1E-8, to avoid division by zero

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
    X_train, X_test, Y_train, Y_test = train_test_split(np.array(f['x']), np.array(f['y']), test_size=param_TEST_SIZE, random_state=param_RANDOM_STATE)

print("Train set size:",len(X_train))
print("Test set size:",len(X_test))

### BUILD MODEL ###

intron_exon_input = layers.Input(shape=(param_SPAN, X_train.shape[2]), name="intron_exon_3acc")
exon_intron_input = layers.Input(shape=(param_SPAN, X_train.shape[2]), name="exon_intron_5don")

if param_MODEL=="LSTM":
    print('Building LSTM model...')
    intron_exon_rnn = layers.LSTM(param_HIDDEN_STATE, return_sequences=True)(intron_exon_input)
    exon_intron_rnn = layers.LSTM(param_HIDDEN_STATE, return_sequences=True)(exon_intron_input)
    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.LSTM(param_HIDDEN_STATE, return_sequences=False)(merged)

elif param_MODEL=="GRU":
    print('Building GRU model...')
    intron_exon_rnn = layers.GRU(param_HIDDEN_STATE, return_sequences=True)(intron_exon_input)
    exon_intron_rnn = layers.GRU(param_HIDDEN_STATE, return_sequences=True)(exon_intron_input)
    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.GRU(param_HIDDEN_STATE, return_sequences=False)(merged)

elif param_MODEL=="RNN":
    print('Building SimpleRNN model...')
    intron_exon_rnn = layers.SimpleRNN(param_HIDDEN_STATE, return_sequences=True)(intron_exon_input)
    exon_intron_rnn = layers.SimpleRNN(param_HIDDEN_STATE, return_sequences=True)(exon_intron_input)
    merged = layers.concatenate([intron_exon_rnn, exon_intron_rnn],axis=1)
    merged_rnn = layers.SimpleRNN(param_HIDDEN_STATE, return_sequences=False)(merged)

else:
    print('-m or --model parameter not recognized...')
    sys.exit(1)

merged_dropout = layers.Dropout(param_DROPOUT)(merged_rnn)
merged_output = layers.Dense(1, activation=param_ACTIVATION)(merged_dropout)
model = models.Model(inputs=[intron_exon_input, exon_intron_input], outputs=merged_output)
model.compile(optimizer=param_OPTIMIZER,loss='binary_crossentropy',metrics=['acc'])
model.summary()

### TRAIN ###

print('Train...')
# history = model.fit([X_train[:,:SPAN,:], X_train[:,SPAN:,:]], Y_train, epochs=EPOCHS, validation_split=TEST_SIZE, batch_size=BATCH_SIZE, verbose=VERBOSE)
history = model.fit([X_train[:,:param_SPAN,:], X_train[:,param_SPAN:,:]], Y_train, epochs=param_EPOCHS, validation_data=([X_test[:,:param_SPAN,:], X_test[:,param_SPAN:,:]], Y_test), batch_size=param_BATCH_SIZE, verbose=param_VERBOSE, shuffle=False)

### PREDICT ###

Y_pred = model.predict([X_test[:,:param_SPAN,:], X_test[:,param_SPAN:,:]], batch_size=param_BATCH_SIZE, verbose=param_VERBOSE)

### SAVE DATA ###

model_io.save2npy(param_PREFIX+"_X_test.npy",X_test)
model_io.save2npy(param_PREFIX+"_Y_test.npy",Y_test)
model_io.save2npy(param_PREFIX+"_Y_pred.npy",Y_pred)

### EVALUATE ###

loss, acc = model.evaluate([X_test[:,:param_SPAN,:], X_test[:,param_SPAN:,:]], Y_test, batch_size=param_BATCH_SIZE, verbose=param_VERBOSE)
print('Test Loss:', loss)
print('Test Accuracy:', acc)

### PLOT LOSS ###

model_eval.plot_loss(history, param_PREFIX)

### PLOT ROC curve ###

model_eval.plot_roc(Y_test, Y_pred, param_PREFIX)
print('Test ROC AUC:', model_eval.calc_roc_auc_score(Y_test, Y_pred))

### PLOT PR curve ###

model_eval.plot_pr(Y_test, Y_pred, param_PREFIX)
print('Test F1 Score:', model_eval.calc_f1_score(Y_test, Y_pred))

### SAVE MODEL+WEIGHT ###

model_io.save(param_PREFIX, model)