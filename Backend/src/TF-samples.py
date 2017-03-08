#! ../ENV/bin/python
import sys
import os
import wave

from modules import audio

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api

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

getLinearModel(0, 0)
print "gud"