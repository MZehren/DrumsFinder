import operator

import numpy as np
import theano
import theano.tensor as T
import lasagne


def charToVect(char, dict):
    result = [0 for i in dict]
    result[dict[char]] = 1
    return result

def vectToChar(vector, reverseDict):
    maxPosition, maxValues = max(enumerate(vector),  key=operator.itemgetter(1))
    return reverseDict[maxPosition]


data = ""
with open("nietzsche.txt", "r") as dataFile: 
    data = dataFile.read().lower()
    
charSet = {key: pos for pos, key in enumerate(set(data))}
reverseLookup = {pos: key for pos, key in enumerate(charSet)}

sequenceLength = 10
numberOfFeature = 3
def gen(offset, size):
    x = [[charToVect(data[offset + i], charSet) for i in range(size)]] #batch of sequence of vector for the input
    y = [charToVect(data[offset+size], charSet)] #batch of vectors of true distribution (we have cut the sequence, as we want to predict the result)
    
    return x, np.array(y,dtype='int32')

# vect = charToVect(data[0], charSet)
# char = vectToChar(vect, reverseLookup)


print("Building network ...")
# First, we build the network, starting with an input layer
# Recurrent layers expect input of shape
# (batch size, SEQ_LENGTH, number of features)
l_in = lasagne.layers.InputLayer(shape=(1,sequenceLength,numberOfFeature,)) #todo: see the difference between seLengt = 10, seLengt = 1 and by removing this dimension

# We now build the LSTM layer which takes l_in as the input layer
# We clip the gradients at GRAD_CLIP to prevent the problem of exploding gradients. 
l_forward_1 = lasagne.layers.LSTMLayer(
    l_in, 512, grad_clipping=100,
    nonlinearity=lasagne.nonlinearities.tanh)

l_forward_2 = lasagne.layers.LSTMLayer(
    l_forward_1, 512, grad_clipping=100,
    nonlinearity=lasagne.nonlinearities.tanh)
# The l_forward layer creates an output of dimension (batch_size, SEQ_LENGTH, N_HIDDEN)
# Since we are only interested in the final prediction, we isolate that quantity and feed it to the next layer. 
# The output of the sliced layer will then be of size (batch_size, N_HIDDEN)
l_forward_slice = lasagne.layers.SliceLayer(l_forward_2, -1, 1)

# The sliced output is then passed through the softmax nonlinearity to create probability distribution of the prediction
# The output of this stage is (batch_size, vocab_size)
l_out = lasagne.layers.DenseLayer(l_forward_slice, num_units=numberOfFeature, W = lasagne.init.Normal(), nonlinearity=lasagne.nonlinearities.sigmoid)

# Theano tensor for the targets
target_values = T.imatrix('target_output')
    
# lasagne.layers.get_output produces a variable for the output of the net
network_output = lasagne.layers.get_output(l_out)

# The loss function is calculated as the mean of the (categorical) cross-entropy between the prediction and target.
cost = lasagne.objectives.binary_crossentropy(network_output,target_values).mean()

# Compute AdaGrad updates for training
print("Computing updates ...")
# Retrieve all parameters from the network
all_params = lasagne.layers.get_all_params(l_out)
    
updates = lasagne.updates.adagrad(cost, all_params, 0.01)
    
# Theano functions for training and computing cost
print("Compiling functions ...")
train = theano.function([l_in.input_var, target_values], cost, updates=updates, allow_input_downcast=True) #todo: try without downcast, it may trunk the float in int !
probs = theano.function([l_in.input_var],network_output,allow_input_downcast=True)

beat = [
        [1,0,1],
        [1,0,0],
        [1,1,0],
        [1,0,0]
    ]
pas = 100
costMean = 0
for i in range(0, 2000):
    x = [[beat[j % len(beat)] for j in range(i, i + sequenceLength)]]
    y = [beat[(i+sequenceLength) % len(beat)]]
    lastCost = train(x, y)
    costMean += lastCost
    if i != 0 and i % pas == 0:
        print 
        print lastCost
        print costMean / pas
        if costMean / pas < 0.1:
            break
   
        costMean = 0

#with real input
for i in range(10):
    lastResult = [[beat[j % len(beat)] for j in range(i, i + sequenceLength)]]
    result = probs(lastResult)

#     lastResult = [lastResult[0][1:sequenceLength] + result[0]]
    
    print ''
    print lastResult
    print [result]
    lastResult =  [result]

# print "-----------------------"
# #with output as input
# lastResult = [[beat[j % len(beat)] for j in range(i, i + sequenceLength)]]
# for i in range(10):
#     lastResult = [[beat[j % len(beat)] for j in range(i, i + sequenceLength)]]
#     result = probs(lastResult)
# 
#     print ''
#     print lastResult
#     lastResult = [result[0]]

# #train
# pas = 100
# costMean = 0
# for i in range(0, 4000):
#     x,y  = gen(i, sequenceLength)
#     costMean += train(x, y)
#     if i % pas == 0:
#         print str(i) + " / " + str(len(data)/2)
#         print costMean / pas
#         costMean = 0
# 
# 
# 
# #test it
# lastResult, unusedY = gen(300, 1)
# for i in range(100):
#     result = probs(lastResult)
#     lastResult = [result] #batch size of 1 remember ?
#     resultChar = vectToChar(result[0], reverseLookup)
#     
#     print resultChar
# #     print result

