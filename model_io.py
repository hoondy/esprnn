#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2017"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Donghoon Lee"
__email__ = "donghoon.lee@yale.edu"

from keras.models import model_from_json, model_from_yaml

def loadModel(MODEL_NAME):

    print('Loading Model..')

    model = model_from_yaml(open(MODEL_NAME+'.yaml').read())
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.load_weights(MODEL_NAME+'.h5')
    model.summary()

    print('Done')

    return model

def saveModel(MODEL_NAME, model):

    open(MODEL_NAME+'.yaml', 'w').write(model.to_yaml())
    model.save_weights(MODEL_NAME+'.h5')