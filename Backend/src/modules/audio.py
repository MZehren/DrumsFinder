import sys
import os
import math

import tensorFlowUtils
# import midiProxy 

import pylab as pl
from scipy.io import wavfile
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle


#load a music file
#currrently only wave is implemented
def load(path):
    return wavfile.read(path)

#load a folder of samples to create a training set
def loadFolder(path, xShape=(1024,32), trainingPercentage=0.9, frameDurationSample=2048, windowStepSample=512):
    X = []
    Y = []
    songs = {}
    classes = {}
    for root, dirs, files in os.walk(path):
        for idx, file in enumerate(files):
#             if idx > 1:
#                 break
            
            if file.endswith(".wav"):
                path = (os.path.join(root, file))
                wave = load(path)
                spectrogram, samplingRate = performFFTs(wave, frameDurationSample=frameDurationSample, windowStepSample=windowStepSample)
                xn = np.fliplr(np.array([fft["frequencies"] for i,fft in enumerate(spectrogram) if i<32])).transpose()

                if xn.shape[1]>=xShape[1]:
                    if root not in classes:
                        classes[root]=len(classes)
                    y = classes[root]
                    
                    if y not in songs:
                        songs[y]= []
                    songs[y].append(xn)
                
                print path
#                 if "snares" in path :
#                     visualizeSpectrogram(wave=wave, spectrogram=spectrogram, samplingRate=samplingRate, frameDuration=frameDurationSample * samplingRate, name=path)

    
    maxSamples = min([len(samples) for label, samples in songs.iteritems()])
    maxLabel = max([label for label, samples in songs.iteritems()])
    for label, samples in songs.iteritems():
        y = tensorFlowUtils.computeOneHotArray(label, maxLabel+1)
        shuffle(samples)
        for i in range(maxSamples):
            X.append(samples[i])
            Y.append(y)
    #shuffle the songs 
    
    return np.array(X), np.array(Y)

# def getFFT(path):    
#     fs, data = wavfile.read(path) # load the data
#     a = data.T[0] # this is a two channel soundtrack, I get the first track
#     b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
#     b=a
#     c = fft(b) # calculate fourier transform (complex numbers list)
#     d = len(c)/2  # you only need half of the fft list (real signal symmetry)
#     plt.plot(abs(c[:(d-1)]),'r') 
#     plt.show()
    

# def write(path, rate, data):
#     wavfile.write(path, rate, data)
    
# def filterRange(matrix, upperLimit = -20, lowerLimit = -120):
#     upperMask = matrix[:,:] > upperLimit
#     matrix[upperMask] = lowerLimit
#     
#     lowerMask = matrix[:,:] < lowerLimit
#     matrix[lowerMask] = lowerLimit
#     
#     return matrix


#duration is in seconds
#sampling is in Hz
#thus the highest calculable frequency is samplingRate / 2
#the lowest calculable frequency is 1/duration, but y[0] correspond to sum(x)
# The number of frequencies calculated are the number of samples / 2. And they are distributed evenly between 0 and the highest one.
def getFrequencies(sampleNumber, samplingRate):
    frequencies = np.fft.fftfreq(int(sampleNumber), d = 1/float(samplingRate))
    return frequencies[0: int(pl.ceil(sampleNumber/2)) ] #we used only half the data points
    #return np.linspace(0.0, (samplingRate / 2), sampleNumber / 2 + 1) #todo: why is it +1 ?

#plot an audio wave, the spectrogram from the fft, or a midi. 
def visualizeSpectrogram(wave=None, spectrogram=None, midi=None, name=None, samplingRate=44100, frameDuration=0.075):

    fig, (wavePlot, spectrogramPlot) = plt.subplots(2)
    
    if name:
        plt.title(name)
        
    if wave:
        wavePlot.plot(np.linspace(0, len(wave[1])/float(wave[0]), num=len(wave[1])), np.array(wave[1]) , "r")
        
 
    if spectrogram:
        #todo: specify zmin, zmax (for colors)
        
        frequenciesBoundaries = getFrequencies(len(spectrogram[0]["frequencies"]), samplingRate)
        extent = [0, spectrogram[-1]["stopTime"], frequenciesBoundaries[0], frequenciesBoundaries[-1]] # [xmin, xmax, ymin, ymax], xmax is the starting time of the last fft done
        points = np.fliplr(np.array([fft["frequencies"] for fft in spectrogram])).transpose()
        cax = spectrogramPlot.imshow(points, extent=extent,  cmap="nipy_spectral", aspect="auto") #todo: Image data can not convert to float. I don't understand this error.
        fig.colorbar(cax)
 
#     if midi:
#         for noteIdx in range(len(midi[0]["notes"])): #each note from the array [1, 0, 0, 0, 1]
#             note = midiProxy.vectorToNote[noteIdx]
#             thisNoteEventsTime = [event["startTime"] for event in midi if event["notes"][noteIdx]]
#             thisNoteEventsHeight = [midiProxy.noteToFrequency[note] for i in range(len(thisNoteEventsTime))]
#             plt.plot(thisNoteEventsTime, thisNoteEventsHeight, midiProxy.noteToPlotIcon[note])
 
 
#     spectrogramPlot.ylabel("frequencies (Hz)")
#     spectrogramPlot.xlabel("time (s)")
    plt.show()
    
  





    
# #frame duration shouldn't be below 0.1s, as the lowest frequency heard is 20Hz. 20Hz is one oscillation each 0.05s. If the frame is shorter than twice the distance, we can't find those frequencies which may help (as we hear them).
#TODO: do not create a dictionnary, create a matrix right away
def performFFTs(waveForm, frameDurationSample=2048, windowStepSample=2048):
    samplingRate = waveForm[0]
    normalizedSound = waveForm[1] #/ (2.**15) #divide each point by 2^15 to normalize. 2^15 is because of the encoding of the waveForm 
    channel0=0
    if len(waveForm[1].shape) != 1 :
        channel0 = normalizedSound[:,0] #todo: use both entries
    else :
        channel0 = normalizedSound
         
    result = []
    cursor = 0
    while cursor + frameDurationSample < len(channel0) : #for each frame
        frame = channel0[int(cursor): int(cursor + frameDurationSample)]
        startTime = float(cursor) / samplingRate
        cursor += windowStepSample
        stopTime = float(cursor) / samplingRate
         
        amplitude = np.fft.fft(frame)
        length = len(frame)
         
        #the fourier transform of the tone returned by the fft function contains both magnitude and phase information and is given in a complex representation (i.e. returns complex numbers). 
        #By taking the absolute value of the fourier transform we get the information about the magnitude of the frequency components.
        nUniquePts = pl.ceil((length + 1 ) / 2.0)
        amplitude = amplitude[1:int(nUniquePts)] #Since FFT is symmetric over it's centre, half the values are just enough. the first value is the mean
        amplitude = abs(amplitude)
 
        amplitude = [value if value > 0 else 10 for value in amplitude] #TODO: direty hack here to prevent some volue to be infinite
 
        # scale by the number of points so that the magnitude does not depend on the length of the signal or on its sampling frequency  
        #amplitude = amplitude / float(length)
         
        #amplitude = amplitude / 32768 #todo: only ogr 16 bits https://fr.wikipedia.org/wiki/D%C3%A9cibel_pleine_%C3%A9chelle_(dB_FS)
        #amplitude = amplitude ** 2  # square it to get the power spectrum from the amplitude
         
 
        #if length % 2 > 0: # we've got odd number of points fft
        #    amplitude[1:len(amplitude)] = amplitude[1:len(amplitude)] * 2
        #else:
        #    amplitude[1:len(amplitude) -1] = amplitude[1:len(amplitude) - 1] * 2 # we've got even number of points fft
 
 
        #use a logarithmic scale
        amplitude = np.log10(amplitude)
        result.append({"startTime": startTime, "stopTime":stopTime, "frequencies": np.array(amplitude)})
 
    #normalize
    max = np.amax([fft["frequencies"] for fft in result])
    min = np.amin([fft["frequencies"] for fft in result])
    for fft in result:
        fft["frequencies"] = [(value - min) / (max - min) for value in fft["frequencies"]]
 
    return result, samplingRate
