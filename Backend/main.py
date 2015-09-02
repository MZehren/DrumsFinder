import numpy as np
from sklearn.preprocessing import normalize

import theano
import theano.tensor as T
import lasagne

import sys
import os
import warnings
import time

import fft
from lasagne.layers.shape import ReshapeLayer

def load_dataset():
    # We first define some helper functions for supporting both Python 2 and 3.
    if sys.version_info[0] == 2:
        from urllib import urlretrieve
        import cPickle as pickle
        def pickle_load(f, encoding):
            return pickle.load(f)
    else:
        from urllib.request import urlretrieve
        import pickle
        def pickle_load(f, encoding):
            return pickle.load(f, encoding=encoding)

    # We'll now download the MNIST dataset if it is not yet available.
    url = 'http://deeplearning.net/data/mnist/mnist.pkl.gz'
    filename = 'mnist.pkl.gz'
    if not os.path.exists(filename):
        print("Downloading MNIST dataset...")
        urlretrieve(url, filename)

    # We'll then load and unpickle the file.
    import gzip
    with gzip.open(filename, 'rb') as f:
        data = pickle_load(f, encoding='latin-1')

    # The MNIST dataset we have here consists of six numpy arrays:
    # Inputs and targets for the training set, validation set and test set.
    X_train, y_train = data[0]
    X_val, y_val = data[1]
    X_test, y_test = data[2]

    # The inputs come as vectors, we reshape them to monochrome 2D images,
    # according to the shape convention: (examples, channels, rows, columns)
    X_train = X_train.reshape((-1, 1, 28, 28))
    X_val = X_val.reshape((-1, 1, 28, 28))
    X_test = X_test.reshape((-1, 1, 28, 28))

    # The targets are int64, we cast them to int8 for GPU compatibility.
    y_train = y_train.astype(np.uint8)
    y_val = y_val.astype(np.uint8)
    y_test = y_test.astype(np.uint8)


    # We just return all the arrays in order, as expected in main().
    # (It doesn't matter how we do this as long as we can read them again.)
    return X_train, y_train, X_val, y_val, X_test, y_test

def loadDataset(trainingFraction=0.7, evalFraction=0.2, testFraction=0.1):
    X = [] #TODO : is it faster to use a npArray here ?
    y = []
    for label, foldername in enumerate(['samples/Kicks', 'samples/HiHats', 'samples/Snares']):
        for filename in os.listdir(foldername):
            path = foldername + '/' + filename
            try: #TODO: why doens't all of them work ?
                results = fft.performFFTs(fft.load(path), frameDuration=0.3) #shape is (number of frames, number of frequencies)
                
                if(len(results) > 0):
                    X.append(results[0]) #TODO, make it dynamic 
                    y.append(label)
            except ValueError:
                warnings.warn("can't open : " + path + "\n" + str(ValueError))

    X = normalize(np.array(X)) # (number of samples, 'number of frames', number of frequencies)
    y = np.array(y) # (number of samples)
    y = y.astype(np.uint8) # The targets are int64, we cast them to int8 for GPU compatibility.
    
    print(X.shape)
    fft.visualizeArray(X)
    
    print(y.shape)
    #We divide the set in 3 different set, shuffled 
    N = len(y)
    indices = np.arange(N)
    np.random.shuffle(indices)
    trainIndices = indices[0:N*trainingFraction]
    evalIndices = indices[N*trainingFraction: N* (trainingFraction + evalFraction)]
    testIndices = indices[N* (trainingFraction + evalFraction) : N]
    
    return X[trainIndices], y[trainIndices], X[evalIndices], y[evalIndices], X[testIndices], y[testIndices]

#  iterating in numpy arrays in minibatchs
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
        yield inputs[excerpt], targets[excerpt] #yield in a for loop will execute a loop each time want to iterate the object returned !


#based on the tuto http://lasagne.readthedocs.org/en/latest/user/tutorial.html#understand-the-mnist-example
def buildMLP(input_var = None):
    #batch size = None, number of frames = None, number of frequencies = 2206
    #input_var it's Theano variable created linked to the input layer
    l_in = lasagne.layers.InputLayer(shape=(None, len(fft.getFrequencies(0.3, 44100))), 
                                     input_var = input_var)
    l_in_drop = lasagne.layers.DropoutLayer(l_in, p=0.2)
    
    l_hid1 = lasagne.layers.DenseLayer(
        l_in_drop, num_units=500, #TODO: which number should we use ?
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.GlorotUniform())
    l_hid1_drop = lasagne.layers.DropoutLayer(l_hid1, p=0.5)

    l_hid2 = lasagne.layers.DenseLayer(
            l_hid1_drop, num_units=500,
            nonlinearity=lasagne.nonlinearities.rectify)
    l_hid2_drop = lasagne.layers.DropoutLayer(l_hid2, p=0.5)
    
    l_out = lasagne.layers.DenseLayer(
        l_hid2_drop, num_units=3,
        nonlinearity=lasagne.nonlinearities.softmax)
    
    return l_out

#from the tuto : http://lasagne.readthedocs.org/en/latest/modules/layers/recurrent.html
def buildLSTM(input_var = None):
    num_inputs = len(fft.getFrequencies(0.3, 44100))
    num_units = 12
    num_classes = 3
    
    l_inp = lasagne.layers.InputLayer((None, None, num_inputs)) #batch_size, sequence_length, num_inputs
    batch_size, sequence_length, _ = l_inp.input_var.shape #retreive a link to the input variable's shape
    
    l_lstm = lasagne.layers.LSTMLayer(l_inp, num_units=num_units)
    
    l_shp = lasagne.layers.ReshapeLayer(l_lstm, (-1, num_units)) #to connect the recurrent layer to the dense layer, we have to flatten the first two dimension (batch and sequence).  
    l_dense = lasagne.layers.DenseLayer(l_shp, num_units = num_classes)
    
    l_out = lasagne.layers.ReshapeLayer(l_dense, (batch_size, sequence_length, num_classes)) #we reshape back to the original shape
    
    return l_out

print("Loading Data ...")
X_train, y_train, X_val, y_val, X_test, y_test = loadDataset()

print("Building model and compiling functions...")
# Prepare Theano variables for inputs and targets
input_var = T.matrix('inputs')
target_var = T.ivector('targets')
# Create neural network model
network = buildMLP(input_var)

#Continuing, we create a loss expression to be minimized in training:
prediction = lasagne.layers.get_output(network)
loss = lasagne.objectives.categorical_crossentropy(prediction, target_var)
loss = lasagne.objectives.aggregate(loss, mode='mean')


#we create a update expression for training using SGB (implemented by nesterov_momentum)
params = lasagne.layers.get_all_params(network, trainable=True)
updates = lasagne.updates.nesterov_momentum(
        loss, params, learning_rate=0.01, momentum=0.9)


#For monitoring, we create the same loss, but getting the output by specifying to remove all non deterministic implementation (thus removing the dropout)
test_prediction = lasagne.layers.get_output(network, deterministic=True)
test_loss = lasagne.objectives.categorical_crossentropy(test_prediction,
                                                        target_var)
test_loss = lasagne.objectives.aggregate(test_loss, mode='mean')
test_acc = T.mean(T.eq(T.argmax(test_prediction, axis=1), target_var),
                  dtype=theano.config.floatX)

#now we compile the theanos expressions by creating function:
#taking the training set as input and retreiving the loss
#it also execute the update expression
train_fn = theano.function([input_var, target_var], loss, updates=updates)

#same here, without update
val_fn = theano.function([input_var, target_var], [test_loss, test_acc])


print("Starting training...")
num_epochs = 500
miniBacthSize = 10
for epoch in range(num_epochs):
    # In each epoch, we do a full pass over the training data:
    train_err = 0
    train_batches = 0
    start_time = time.time()
    for batch in iterate_minibatches(X_train, y_train, miniBacthSize, shuffle=True):
        inputs, targets = batch
        train_err += train_fn(inputs, targets)
        train_batches += 1

    # And a full pass over the validation data:
    val_err = 0
    val_acc = 0
    val_batches = 0
    for batch in iterate_minibatches(X_val, y_val, miniBacthSize, shuffle=False):
        inputs, targets = batch
        err, acc = val_fn(inputs, targets)
        val_err += err
        val_acc += acc
        val_batches += 1

    # Then we print the results for this epoch:
    print("Epoch {} of {} took {:.3f}s".format(
        epoch + 1, num_epochs, time.time() - start_time))
    print("  training loss:\t\t{:.6f}".format(train_err / train_batches))
    print("  validation loss:\t\t{:.6f}".format(val_err / val_batches))
    print("  validation accuracy:\t\t{:.2f} %".format(
        val_acc / val_batches * 100))
    
# After training, we compute and print the test error:
test_err = 0
test_acc = 0
test_batches = 0
for batch in iterate_minibatches(X_test, y_test, len(X_test), shuffle=False):
    inputs, targets = batch
    err, acc = val_fn(inputs, targets)
    test_err += err
    test_acc += acc
    test_batches += 1
print("Final results:")
print("  test loss:\t\t\t{:.6f}".format(test_err / test_batches))
print("  test accuracy:\t\t{:.2f} %".format(
    test_acc / test_batches * 100))

# Optionally, you could now dump the network weights to a file like this:
#np.savez('model.npz', lasagne.layers.get_all_param_values(network))
