#! ../ENV/bin/python
import sys
import os
import wave

from modules import audio
from modules import tensorFlowUtils

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from tensorflow.contrib.metrics.python.metrics.classification import accuracy
from sympy.physics.units import ten
from tensorflow.contrib.slim.python.slim.model_analyzer import tensor_description


def getLinearModel(xShape, yShape):
    x = tf.placeholder(tf.float32, [None, 32768]) #xShape could be [None, 1024, 32]
    W = tf.Variable(tf.random_normal([32768, 3], stddev=0.35))
    b = tf.Variable(tf.zeros([3]))
    
    y = tf.nn.softmax(tf.matmul(x, W) + b)
    y_ = tf.placeholder(tf.float32, [None, 3])
#     cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    
    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    
    
    # loadFolder("../../Data/samples/tabs/test 0.075")
    X, Y_ = audio.loadFolder("../../Data/samples/sampleradar-32bit")
    X = np.reshape(X, (-1, 32768))
    
    print X.dtype
    print Y_.dtype
    for _ in range(1000):
        print "\nbatch :", _ 
        print "accuracy :", sess.run(accuracy, feed_dict={x: X, y_: Y_})
#         print "W :", sess.run(W)
#         print "b :", sess.run(b)
        #print "y :", sess.run(y, feed_dict={x: X})
#         print "x :", sess.run(x, feed_dict={x: X})
        print "cross_entropy", sess.run(cross_entropy, feed_dict={x: X, y_: Y_})
        
        sess.run(train_step, feed_dict={x: X, y_: Y_})
    print "y :", sess.run(y, feed_dict={x: X})

#init weights
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

#init bias
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)
  
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def getConvModel():
    W_conv1 = weight_variable([5, 5, 1, 32]) # patch of 5 by 5 on 1 channel with 32 outputs
    b_conv1 = bias_variable([32])
    
    x = tf.placeholder(tf.float32, [None, 1024, 32, 1]) #images de 1024 par 32 pixels avec 1 channel
    y_ = tf.placeholder(tf.float32, [None, 3])  
    
    h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # second layer     
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    
    #densely connected layer
    W_fc1 = weight_variable([256 * 8 * 64, 1024])
    b_fc1 = bias_variable([1024])
    
    h_pool2_flat = tf.reshape(h_pool2, [-1, 256*8*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
    
    #dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
    
    #Readout
    W_fc2 = weight_variable([1024, 3])
    b_fc2 = bias_variable([3])
    
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    
    
    #learn
    sess = tf.InteractiveSession()
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess.run(tf.global_variables_initializer())
    
    X, Y_ = audio.loadFolder("../../Data/samples/sampleradar-32bit")
    X = np.reshape(X, (-1, 1024, 32, 1))
    for i in range(20000):
        if i%10 == 0:
            train_accuracy = accuracy.eval(feed_dict={x:X, y_: Y_, keep_prob: 1.0})
            print("step %d, training accuracy %g"%(i, train_accuracy))
        train_step.run(feed_dict={x: X, y_: Y_, keep_prob: 0.5})
    
#     print("test accuracy %g"%accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

def getConvMultiLabelModel():
    modelSerialisationName = "../../Data/models/1"
    sess = tf.InteractiveSession()    
 
    #create model
    W_conv1 = weight_variable([5, 5, 1, 32]) # patch of 5 by 5 on 1 channel with 32 outputs
    b_conv1 = bias_variable([32])
    
    x = tf.placeholder(tf.float32, [None, 1024, 32, 1]) #images de 1024 par 32 pixels avec 1 channel
    y_ = tf.placeholder(tf.float32, [None, 6])  
    
    h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # second layer     
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    
    #densely connected layer
    W_fc1 = weight_variable([256 * 8 * 64, 1024])
    b_fc1 = bias_variable([1024])
    
    h_pool2_flat = tf.reshape(h_pool2, [-1, 256*8*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
    
    #dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
    
    #Readout
    W_fc2 = weight_variable([1024, 6])
    b_fc2 = bias_variable([6])
    
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    
    
    #learn
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    
    #TODO: Y should be 0 and 1 or -1 and 1 ?   
    prediction = tf.greater(y_conv, tf.constant(0.5)) 
    correct_prediction = tf.equal(prediction, tf.greater(y_,tf.constant(0.5)))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    #correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    
    #load model
    if os.path.isfile(modelSerialisationName):
        print "load model"
        saver.restore(sess, modelSerialisationName)
        
    #train model
    for i in range(10):
        print "\n", str(i), "load data"
        X, Y_, XTest, Y_Test = audio.loadSamplesFolder("../../Data/samples/testAtlantis/train", fileLimit=100)
        X = np.reshape(X, (-1, 1024, 32, 1))
        XTest = np.reshape(XTest, (-1, 1024, 32, 1)) 

        for epoch in range(10):
            #  if epoch%100 == 0:
            #    train_accuracy = accuracy.eval(feed_dict={x:X, y_: Y_, keep_prob: 1.0})
            #    print("step %d, training accuracy %g"%(epoch, train_accuracy))
            train_step.run(feed_dict={x: X, y_: Y_, keep_prob: 0.5})
        
        #test model
        test_accuracy = accuracy.eval(feed_dict={x:XTest, y_: Y_Test, keep_prob: 1.0})
        print("Test accuracy", test_accuracy)
        print Y_Test
        print sess.run(y_conv, feed_dict={x:XTest, keep_prob: 1.0})
        print sess.run(prediction, feed_dict={x:XTest, keep_prob: 1.0})
        print "model saved : ", saver.save(sess, modelSerialisationName)

def myGetConvMultiLabelModel():
    modelSerialisationName = "../../Data/models/1"
    sess = tf.InteractiveSession()    
 
    #create model
    W_conv1 = weight_variable([10, 10, 1, 32]) # patch of 5 by 5 on 1 channel with 32 outputs
    b_conv1 = bias_variable([32])
    
    x = tf.placeholder(tf.float32, [None, 1024, 32, 1]) #images de 1024 par 32 pixels avec 1 channel
    y_ = tf.placeholder(tf.float32, [None, 6])  
    
    h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # second layer     
    W_conv2 = weight_variable([128, 5, 32, 64])
    b_conv2 = bias_variable([64])
    
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    
    #densely connected layer
    W_fc1 = weight_variable([256 * 8 * 64, 1024])
    b_fc1 = bias_variable([1024])
    
    h_pool2_flat = tf.reshape(h_pool2, [-1, 256*8*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
    
    #dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
    
    #Readout
    W_fc2 = weight_variable([1024, 6])
    b_fc2 = bias_variable([6])
    
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    
    
    #learn
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    
    #TODO: Y should be 0 and 1 or -1 and 1 ?   
    prediction = tf.greater(y_conv, tf.constant(0.5)) 
    correct_prediction = tf.equal(prediction, tf.greater(y_,tf.constant(0.5)))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    #correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    
    #load model
    if os.path.isfile(modelSerialisationName + ".index"):
        print "load model"
        saver.restore(sess, modelSerialisationName)
        
    #train model
    for i in range(10):
        print "\n", str(i), "load data"
        X, Y_ = audio.loadSamplesFolder("../../Data/samples/testAtlantis/train", fileLimit=100, windowStepSample=128)
        print X.shape
        X = np.reshape(X, (-1, 1024, 32, 1))

        for epoch in range(10):
            train_step.run(feed_dict={x: X, y_: Y_, keep_prob: 0.5})
        

    #test model
    X, Y_ = audio.loadSamplesFolder("../../Data/samples/testAtlantis/test", fileLimit=100, windowStepSample=128)
    X = np.reshape(X, (-1, 1024, 32, 1))
    test_accuracy = accuracy.eval(feed_dict={x:X, y_:Y ,keep_prob: 1.0})
    print("Test accuracy", test_accuracy)
    print Y
    print sess.run(y_conv, feed_dict={x:X, keep_prob: 1.0})
    print sess.run(prediction, feed_dict={x:X, keep_prob: 1.0})
    print "model saved : ", saver.save(sess, modelSerialisationName)
   
myGetConvMultiLabelModel()
# getConvModel()
# getLinearModel(0, 0)
print "gud"