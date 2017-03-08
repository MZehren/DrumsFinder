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
    x = tf.placeholder(tf.float32, [None, 1024, 32]) #xShape could be [None, 1024, 32]
    W = tf.Variable(tf.zeros([1024, 32, 3]))
    b = tf.Variable(tf.zeros([3]))
    
    y = tf.nn.softmax(tf.matmul(x, W) + b)
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

getLinearModel(0,0)

# loadFolder("../../Data/samples/tabs/test 0.075")
X, Y = audio.loadFolder("../../Data/samples/sampleradar-32bit")
print Y
print X.shape
print Y.shape


print "gud"