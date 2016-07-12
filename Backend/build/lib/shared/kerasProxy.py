import os
import fractions
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout
import numpy as np

  
def getLSTMModel(maxLength, numFeatures):
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(maxLength, numFeatures)))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(numFeatures))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    
    return model

def trainModel(model, song, maxLength):

    X_train = [[song[i] for i in range(start, start + maxLength) ] for start in range(0, len(song)-maxLength)]
    Y_train = [song[i] for i in range(maxLength, len(song))]
    
    model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)
    
def testModel(model, maxLength):
#         36 : 0,
#         40 : 1,
#         41 : 2,
#         45 : 3,
#         48 : 4,
#         42 : 5,
#         46 : 6,
#         49 : 7,
#         51 : 8
    X_tests = [
        [
            [1,0,0,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,0,1],
        ],
        [
            [1,0,0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
        ]
    ]
    for X_test in X_tests:
        X_test = [X_test[i % len(X_test)] for i in range(maxLength)]
        Y = X_test[maxLength % len(X_test)]
        
        classes = model.predict_classes(np.asarray([X_test]), batch_size=1)
        proba = model.predict_proba(np.asarray([X_test]), batch_size=1)
        
        print X_test
        print Y
        print classes
        print proba
        print


    