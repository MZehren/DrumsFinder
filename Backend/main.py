import numpy as np
import theano
import theano.tensor as T
import lasagne

import os
import warnings
import fft
from sympy.core.numbers import RealNumber

def loadDataset():
    X = [] #TODO : is it faster to use a npArray here ?
    y = []
    for label, foldername in enumerate(['samples/Kicks', 'samples/Snares', 'samples/HiHats']):
        for filename in os.listdir(foldername):
            path = foldername + '/' + filename
            try:
                results = fft.performFFTs(fft.load(path)) #shape is (number of frames, number of frequencies)
                
                if(len(results) > 4):
                    X.append(results[0:5]) #TODO, make it dynamic 
                    y.append(label)
            except ValueError:
                warnings.warn("can't open : " + path + "\n" + str(ValueError))

    
    numbreFreq = len(fft.getFrequencies(0.1, 44100))
    RealNumberFreq = len(X[0][0])
    X = np.array(X) # (number of samples, number of frames, number of frequencies)
    y = np.array(y) # (number of samples)
    return X, y

#iterating in numpy arrays in minibatchs
def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


#based on the tuto http://lasagne.readthedocs.org/en/latest/user/tutorial.html#understand-the-mnist-example
def buildMLP(input_var = None):
    #batch size = None, number of frames = None, number of frequencies = 2006
    #input_var it's Theano variable created linked to the input layer
    l_in = lasagne.layers.InputLayer(shape=(None, 5, len(fft.getFrequencies(0.1, 44100))), 
                                     input_var = input_var)
    l_in_drop = lasagne.layers.DropoutLayer(l_in, p=0.2)
    
    l_hid1 = lasagne.layers.DenseLayer(
        l_in_drop, num_units=800,
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform())
    l_hid1_drop = lasagne.layers.DropoutLayer(l_hid1, p=0.5)

    l_hid2 = lasagne.layers.DenseLayer(
            l_hid1_drop, num_units=800,
            nonlinearity=lasagne.nonlinearities.rectify)
    l_hid2_drop = lasagne.layers.DropoutLayer(l_hid2, p=0.5)
    
    l_out = lasagne.layers.DenseLayer(
        l_hid2_drop, num_units=10,
        nonlinearity=lasagne.nonlinearities.softmax)
    
    return l_out


def buildLSTM():
    return "TODO"



X, y = loadDataset()
# Prepare Theano variables for inputs and targets
input_var = T.tensor3('inputs')
target_var = T.ivector('targets')
# Create neural network model
network = buildMLP(None)

#Continuing, we create a loss expression to be minimized in training:
prediction = lasagne.layers.get_output(network)
loss = lasagne.objectives.categorical_crossentropy(prediction, target_var)
loss = loss.mean()

for batch in iterate_minibatches(X, y, 10, shuffle=True):
    inputs, targets = batch
    print(targets)
