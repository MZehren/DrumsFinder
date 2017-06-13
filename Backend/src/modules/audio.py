import sys
import os
import math

import tensorFlowUtils
import midiProxy 

import pylab as pl
from scipy.io import wavfile
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
from matplotlib.cbook import Null



#load a music file
#currrently only wave is implemented
def load(path):
    return wavfile.read(path)

def write(path, rate, data):
    wavfile.write(path, rate, data)

    


'''
Return the Discrete Fourier Transform sample frequencies
'''
def getFrequenciesHz(sampleNumber, samplingRate):
    frequencies = np.fft.rfftfreq(int(sampleNumber), d = 1/float(samplingRate))
    return frequencies[0: int(pl.ceil(sampleNumber/2)) ] #we used only half the data points
    #return np.linspace(0.0, (samplingRate / 2), sampleNumber / 2 + 1) #todo: why is it +1 ?

'''
Return the mel frequencies
'''
def getFrequenciesMel(sampleNumber, samplingRate):
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (samplingRate / 2) / 700))  # Convert Hz to Mel
    return np.linspace(low_freq_mel, high_freq_mel, sampleNumber + 2)  # Equally spaced in Mel scale
   

#plot an audio wave, the spectrogram from the fft, or a midi. 
def visualizeSpectrogram(wave=None, spectrogram=None, midi=None, name=None, samplingRate=44100):

    fig, (wavePlot, spectrogramPlot) = plt.subplots(2)
    
    if name:
        plt.title(name)
        
    if wave:
        wavePlot.plot(np.linspace(0, len(wave[1])/float(wave[0]), num=len(wave[1])), np.array(wave[1]) , "r")
        
 
    if spectrogram:
        #todo: specify zmin, zmax (for colors)
        
        frequenciesBoundaries = getFrequenciesHz(len(spectrogram[0]["frequencies"]), samplingRate)
        extent = [0, spectrogram[-1]["stopTime"], frequenciesBoundaries[0], frequenciesBoundaries[-1]] # [xmin, xmax, ymin, ymax], xmax is the starting time of the last fft done
        points = np.fliplr(np.array([fft["frequencies"] for fft in spectrogram])).transpose()
        cax = spectrogramPlot.imshow(points,  extent=extent, cmap="nipy_spectral", aspect="auto") #todo: Image data can not convert to float. I don't understand this error.
        fig.colorbar(cax)
 
    if midi:
        for noteIdx in range(len(midi[0]["notes"])): #each note from the array [1, 0, 0, 0, 1]
            note = midiProxy.vectorToNote[noteIdx]
            thisNoteEventsTime = [event["startTime"] for event in midi if event["notes"][noteIdx]]
            thisNoteEventsHeight = [midiProxy.noteToFrequency[note] for i in range(len(thisNoteEventsTime))]
            plt.plot(thisNoteEventsTime, thisNoteEventsHeight, midiProxy.noteToPlotIcon[note])
 
 
#     spectrogramPlot.ylabel("frequencies (Hz)")
#     spectrogramPlot.xlabel("time (s)")
    plt.show()
    
  




'''
frame duration shouldn't be below 0.1s, as the lowest frequency heard is 20Hz. 20Hz is one oscillation each 0.05s. 
If the frame is shorter than twice the distance, we can't find those frequencies which may help (as we hear them).
at 44kHz, 10ms = 440 Hz
TODO: do not create a dictionnary, create a matrix right away
see http://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html for a good tutorial
'''
def performFFTs(waveForm, frameDuration=0.025, frameStride=0.01):
    samplingRate = waveForm[0]
    frameDurationSample = int(frameDuration * samplingRate)
    frameStrideSample = int(frameStride * samplingRate)
    
    #normalizedSound = waveForm[1] / (2.**15) #divide each point by 2^15 to normalize. 2^15 is because of the encoding of the waveForm 
    channel0=0
    if len(waveForm[1].shape) != 1 :
        channel0 = (waveForm[1][:,0] + waveForm[1][:,1]) / 2 #todo: use both entries
    else :
        channel0 = waveForm[1]
         
    result = []
    cursor = 0
    while cursor + frameDurationSample < len(channel0) : #for each frame
        frame = channel0[int(cursor): int(cursor + frameDurationSample)]
        
        #apply a hamming window to reduce spectral leakage
        frame *= np.hamming(frameDurationSample)
        
        #Fourier-Transform and Power Spectrum
        NFFT = 512 # number of points in the fft to use
        magnitudeFrame = np.absolute(np.fft.rfft(frame, NFFT))  # Magnitude of the FFT
        powerSpectrumFrame = ((1.0 / NFFT) * ((magnitudeFrame) ** 2))  # Power Spectrum

        #Filter Banks
        filter_banks = filterBanks(powerSpectrumFrame, samplingRate, NFFT)
        
        result.append({"startTime": float(cursor) / samplingRate, "stopTime":float(cursor + frameStrideSample) / samplingRate, "frequencies": np.array(filter_banks)})
        cursor += frameStrideSample
 
    #normalize
    max = np.amax([fft["frequencies"] for fft in result])
    min = np.amin([fft["frequencies"] for fft in result])
    mean = np.mean([fft["frequencies"] for fft in result])
    for fft in result:
        fft["frequencies"] = [(value - min) / (max - min) * 2 - 1 for value in fft["frequencies"]]

    return result, samplingRate





'''
the mel scale is a perceptual scale of pitches judged by listeners to be equal in distance from one another.
'''
def filterBanks(frame, samplingRate, NFFT, nfilter = 40):
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (samplingRate / 2) / 700))  # Convert Hz to Mel
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilter + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = np.floor((NFFT + 1) * hz_points / samplingRate)
    
    fbank = np.zeros((nfilter, int(np.floor(NFFT / 2 + 1))))
    for m in range(1, nfilter + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right
    
        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(frame, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * np.log10(filter_banks)  # dB
    return filter_banks

'''
MFC is a rep
'''
def getMFCC():
    return 0;
