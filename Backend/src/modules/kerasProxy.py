import os
import fractions
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.optimizers import SGD
import numpy as np

  
def getLSTMModel(inputShape=(1,1), outputLength=1):
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=inputShape))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(outputLength))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    
    return model

#thanks https://github.com/kaggle-novice/mnist_keras/blob/master/mnist-keras.py
def getConvModel(inputShape=(1,1), outputLength=1):
    # Sequential wrapper model
    model = Sequential()

    # first convolutional layer
    model.add(Convolution2D(32,1,2,2))
    model.add(Activation('relu'))

    # second convolutional layer
    model.add(Convolution2D(48, 32, 2, 2))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(poolsize=(2,2)))

    # third convolutional layer
    model.add(Convolution2D(32, 48, 2, 2))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(poolsize=(2,2)))

    # convert convolutional filters to flatt so they can be feed to
    # fully connected layers
    model.add(Flatten())

    # first fully connected layer
    model.add(Dense(32*6*6, 128, init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    # second fully connected layer
    model.add(Dense(128, 128, init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    # last fully connected layer which output classes
    model.add(Dense(128, outputLength, init='lecun_uniform'))
    model.add(Activation('softmax'))

    # setting sgd optimizer parameters
    sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='binary_crossentropy', optimizer=sgd)

def trainModel(model, song, maxLength):

    X_train = [[song[i] for i in range(start, start + maxLength) ] for start in range(0, len(song)-maxLength)]
    Y_train = [song[i] for i in range(maxLength, len(song))]
    
    model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)
    
def testModel(model, X, Y):

    classes = model.predict_classes(X, batch_size=1)
    proba = model.predict_proba(X, batch_size=1)

    print Y
    print classes
    print proba
    print

def loadWeights(path, model):
    if os.path.isfile(path):
        model.load_weights(path)

def saveWeights(path, model):
    if os.path.isfile(path):
        model.save_weights(path)