#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2017"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

import argparse, sys
from keras import layers
from keras import models
import model_eval, model_io
import numpy as np
from sklearn.model_selection import train_test_split

### Usage: python model_train.py -n TEST -m LSTM -s 100 -p "/path/to/npyData" -e 50
### -x E123-DNA.exonDef_ss_100.npy,E123-DNase.exonDef_ss_100.npy,E123-H3K27me3.exonDef_ss_100.npy,E123-H3K4me3.exonDef_ss_100.npy
### -y E123-EXP.exonDef_ss_100.npy

parser = argparse.ArgumentParser(description='Train Model')

parser.add_argument('-n','--name', help='model name',required=True)
parser.add_argument('-m','--model', help='RNN model: LSTM,GRU,SimpleRNN',required=True)
parser.add_argument('-s','--span', help='span size from splice site',required=True, type=int)
parser.add_argument('-p','--path', help='path to npy data',required=True)
parser.add_argument('-e','--epoch', help='epoch',required=False, type=int, default=20)
parser.add_argument('-x','--input', help='input npy list, comma-separated',required=True)
parser.add_argument('-y','--output', help='output npy',required=True)

args = parser.parse_args()

###

HIDDEN_SIZE = 4*args.span
DROPOUT = 0.3
BATCH_SIZE = 100
EPOCHS = args.epoch
MODEL_NAME = args.name

### LOAD DATA ###

inputFiles = args.input.split(",")
print "Found",len(inputFiles),"files"

for idx, file in enumerate(inputFiles):
    print "Loading ",file

    if idx==0:
        inputX=np.load(args.path+"/"+file)
    else:
        inputX=np.append(inputX, np.load(args.path+"/"+file), axis=2)

inputY = np.load(args.path+"/"+args.output)

### TRAIN TEST SPLIT ###

print "Splitting data into train and test set"
X_train, X_test, Y_train, Y_test = train_test_split(inputX, inputY, test_size=0.1) #random_state=42 if needed
print "Train set size:",len(X_train)
print "Test set size:",len(X_test)

### SPLIT DATA ###

def splitInput(input):

    input_3acc = input[:,0:input.shape[1]/2,:]
    input_5don = input[:,input.shape[1]/2:input.shape[1],:]

    print "3'ss X:",input_3acc.shape
    print "5'ss X:",input_5don.shape

    return input_3acc,input_5don

X_train_3acc, X_train_5don = splitInput(X_train)
X_test_3acc, X_test_5don = splitInput(X_test)

### BUILD MODEL ###

if args.model=="LSTM":

    print('Building LSTM model...')

    intron_exon_input = layers.Input(shape=(X_train_3acc.shape[1], X_train_3acc.shape[2]), name="intron_exon_3acc")
    intron_exon_rnn = layers.LSTM(HIDDEN_SIZE/2, return_sequences=True)(intron_exon_input)

    exon_intron_input = layers.Input(shape=(X_train_5don.shape[1], X_train_5don.shape[2]), name="exon_intron_5don")
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

    intron_exon_input = layers.Input(shape=(X_train_3acc.shape[1], X_train_3acc.shape[2]), name="intron_exon_3acc")
    intron_exon_rnn = layers.GRU(HIDDEN_SIZE/2, return_sequences=True)(intron_exon_input)

    exon_intron_input = layers.Input(shape=(X_train_5don.shape[1], X_train_5don.shape[2]), name="exon_intron_5don")
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

    intron_exon_input = layers.Input(shape=(X_train_3acc.shape[1], X_train_3acc.shape[2]), name="intron_exon_3acc")
    intron_exon_rnn = layers.SimpleRNN(HIDDEN_SIZE/2, return_sequences=True)(intron_exon_input)

    exon_intron_input = layers.Input(shape=(X_train_5don.shape[1], X_train_5don.shape[2]), name="exon_intron_5don")
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
model.fit([X_train_3acc, X_train_5don], Y_train, epochs=EPOCHS, validation_data=([X_test_3acc, X_test_5don], Y_test), batch_size=BATCH_SIZE, verbose=2)
# verbose: 0 for no logging to stdout, 1 for progress bar logging, 2 for one log line per epoch.

### SAVE DATA ###

model_io(MODEL_NAME, model)

### EVALUATE ###

loss, acc = model.evaluate([X_test_3acc, X_test_5don], Y_test, batch_size=BATCH_SIZE, verbose=1)
print('Test Loss:', loss)
print('Test Accuracy:', acc)

### PREDICT ###

predY = model.predict([X_test_3acc, X_test_5don], batch_size=BATCH_SIZE, verbose=1)
model_eval.save2npy(MODEL_NAME+"_predY.npy",predY)

### ROC AUC ###

print 'Test ROC AUC:', model_eval.calcROC_AUC(Y_test, predY)

### F1 SCORE ###

print 'Test F1 Score:', model_eval.calcF1(Y_test, predY)

### PLOT ROC AUC ###

model_eval.plotROC_AUC(Y_test, predY, MODEL_NAME)
