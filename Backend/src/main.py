#! ../ENV/bin/python
import sys
import os
import wave

from modules import audio
from modules import tensorFlowUtils
from modules import samples

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from tensorflow.contrib.metrics.python.metrics.classification import accuracy
from sympy.physics.units import ten
from tensorflow.contrib.slim.python.slim.model_analyzer import tensor_description
from math import sqrt


def put_kernels_on_grid (kernel, grid_Y, grid_X, pad = 1):

    '''Visualize conv. features as an image (mostly for the 1st layer).
    Place kernel into a grid, with some paddings between adjacent filters.

    Args:
      kernel:            tensor of shape [Y, X, NumChannels, NumKernels]
      (grid_Y, grid_X):  shape of the grid. Require: NumKernels == grid_Y * grid_X
                           User is responsible of how to break into two multiples.
      pad:               number of black pixels around each filter (between them)

    Return:
      Tensor of shape [(Y+2*pad)*grid_Y, (X+2*pad)*grid_X, NumChannels, 1].
    '''

    x_min = tf.reduce_min(kernel)
    x_max = tf.reduce_max(kernel)

    kernel1 = (kernel - x_min) / (x_max - x_min)

    # pad X and Y
    x1 = tf.pad(kernel1, tf.constant( [[pad,pad],[pad, pad],[0,0],[0,0]] ), mode = 'CONSTANT')

    # X and Y dimensions, w.r.t. padding
    Y = kernel1.get_shape()[0] + 2 * pad
    X = kernel1.get_shape()[1] + 2 * pad

    channels = kernel1.get_shape()[2]

    # put NumKernels to the 1st dimension
    x2 = tf.transpose(x1, (3, 0, 1, 2))
    # organize grid on Y axis
    x3 = tf.reshape(x2, tf.stack([grid_X, Y * grid_Y, X, channels])) #3

    # switch X and Y axes
    x4 = tf.transpose(x3, (0, 2, 1, 3))
    # organize grid on X axis
    x5 = tf.reshape(x4, tf.stack([1, X * grid_X, Y * grid_Y, channels])) #3

    # back to normal order (not combining with the next step for clarity)
    x6 = tf.transpose(x5, (2, 1, 3, 0))

    # to tf.image_summary order [batch_size, height, width, channels],
    #   where in this case batch_size == 1
    x7 = tf.transpose(x6, (3, 0, 1, 2))
    # scale to [0, 255] and convert to uint8
    return tf.image.convert_image_dtype(x7, dtype = tf.uint8) 

def weight_variable(shape):
    '''
    create and init weights
    it's better than starting at 0 to prevent a null gradient.
    it's also good to have randomization to prevent symmetry in the network
    And it's good to have a positive initial value to prevent dead ReLu neurons
    '''
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    '''
    create and init bias
    '''
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    '''
    Create a convolutional layer of stride of 1 and no padding
    which means that the output will be the same size as the input.
    x = input tensor [batch, in_height, in_width, in_channels]
    W = filters [filter_height, filter_width, in_channels, out_channels]
        in_channels = each color of the image
        out_channels = activation of each filter
    
    the output is an activation map in 4D as the input
    '''
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    '''
    perform a max pooling
    x is the input tensor of shape [batch, in_height, in_width, in_channels]
    ksize = the size of the window in each dimension
    strides= the stride of the sliding window
    '''
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def inference(x, y_, keep_prob):
    """Build the =model up to where it may be used for inference """
    with tf.name_scope('conv1'):
        # the first layer is a convolutional layer followed by a pooling
        #so we create the filters variable here
        W_conv1 = weight_variable([10, 10, 1, 32]) # patch of 5 by 5 on 1 channel with 32 outputs
        b_conv1 = bias_variable([32])
        
        #the first layer
        h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)
        h_pool1 = max_pool_2x2(h_conv1) #the 2x2 pooling will reduce each the width and the height of the pictures by half
        tf.summary.image("conv1/kernels", put_kernels_on_grid(W_conv1, 4, 8), max_outputs=1)
        
    with tf.name_scope('conv2'):
        # second layer     
        # we stack layers. This one will have 64 features for each 10*10 patch
        W_conv2 = weight_variable([10, 10, 32, 64])
        b_conv2 = bias_variable([64])
        
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)
    
    with tf.name_scope('fullyConnected'):
        #densely connected layer
        #we add a layer of 1024 neurons
        #each neuron is fully connected to the previous input, so 10*12*64
        W_fc1 = weight_variable([10 * 13 * 64, 1024])
        b_fc1 = bias_variable([1024])
        
        #we reshape the output tensor to a 2D tensor which will be plugged in a fully connected layer
        h_pool2_flat = tf.reshape(h_pool2, [-1, 10*13*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        
        #dropout
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
        
        #Readout
        W_fc2 = weight_variable([1024, 6])
        b_fc2 = bias_variable([6])
        
        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    
    return y_conv
#to see a tutorial : https://www.tensorflow.org/get_started/mnist/pros
def getConvMultiLabelModel():
    modelSerialisationName = "../../Data/models/convolutional"
    logSerialisationName = "../../Data/models/logs"
    sess = tf.InteractiveSession() # an interactive session will be used by default for the eval and run operation
 
    #create model
    #we have to reshape the images as a 4D tensor, the first dimension is the minibatch size
    #so we create the input variables here
    global_step = tf.Variable(0, trainable=False) #we store the global step
    x = tf.placeholder(tf.float32, [None, 40, 50, 1]) #X images de 1024 par 32 pixels avec 1 channel
    y_ = tf.placeholder(tf.float32, [None, 6])  
    keep_prob = tf.placeholder(tf.float32) #for dropout
    y_conv = inference(x, y_, keep_prob)
    
    #learn
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y_conv))
    tf.summary.scalar('loss', cross_entropy) #we save the value for the logs
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy, global_step=global_step)
    
    #TODO: Y should be 0 and 1 or -1 and 1 ?   
    prediction = tf.greater(y_conv, tf.constant(0.5)) 
    correct_prediction = tf.equal(prediction, tf.greater(y_,tf.constant(0.5)))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar('accuracy', accuracy)#we save the value for the logs
    
    summary = tf.summary.merge_all()#collect all the summaries into a single Tensor
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    train_writer = tf.summary.FileWriter(logSerialisationName + "/train", sess.graph)
    test_writer = tf.summary.FileWriter(logSerialisationName + "/test")
    
    #load model
    if os.path.isfile(modelSerialisationName + ".index"):
        print "load model"
        saver.restore(sess, modelSerialisationName)
        
    #train model

    while(True):
        step = sess.run(global_step)
        print "\n", str(step), "load data"
        X, Y_ = samples.loadSamplesFolder("../../Data/samples/testAtlantis/train", fileLimit=32)
        print "shape of input :", X.shape
        X = np.reshape(X, (-1, 40, 50, 1)) #reshape to add the last dimension
        train_step.run(feed_dict={x: X, y_: Y_, keep_prob: 0.5})
            
        #log training data
        summary_str = sess.run(summary, {x: X, y_: Y_, keep_prob: 0.5})
        train_writer.add_summary(summary_str, step)
        #test model
        if(step%10 == 0):
            X, Y_ = samples.loadSamplesFolder("../../Data/samples/testAtlantis/test", fileLimit=32)
            X = np.reshape(X, (-1, 40, 50, 1))
            #log test data
            summary_str = sess.run(summary, {x: X, y_: Y_, keep_prob: 0.5})
            test_writer.add_summary(summary_str, step)
#             test_accuracy = accuracy.eval(feed_dict={x:X, y_:Y_ ,keep_prob: 1.0})
#             print("Test accuracy", test_accuracy)
#             print Y_
#             print sess.run(y_conv, feed_dict={x:X, keep_prob: 1.0})
#             print sess.run(prediction, feed_dict={x:X, keep_prob: 1.0})
            print "model saved : ", saver.save(sess, modelSerialisationName)
        

   
   
getConvMultiLabelModel()
print "gud"