from pylab import*
from scipy.io import wavfile

import matplotlib.pyplot as plt
import numpy as np




def load(path):    
    return wavfile.read(path)

def write(path, rate, data):
    wavfile.write(path, rate, data)
    
def filterRange(matrix, upperLimit = -20, lowerLimit = -120):
    upperMask = matrix[:,:] > upperLimit
    matrix[upperMask] = lowerLimit
    
    lowerMask = matrix[:,:] < lowerLimit
    matrix[lowerMask] = lowerLimit
    
    return matrix
#duration is in seconds
#sampling is in Hz
#thus the highest calculable frequency is samplingRate / 2
#the lowest calculable frequency is 1/duration, but y[0] correspond to sum(x)
#The number of frequencies calculated are the number of samples / 2. And they are distributed evenly between 0 and the highest one.
def getFrequencies(duration, samplingRate):
    sampleNumber = duration * samplingRate
    
    fftFreq = np.fft.fftfreq(int(sampleNumber), duration)
    return np.linspace(0.0, (samplingRate / 2), sampleNumber / 2 + 1) #todo: why is it +1 ?

def visualizeArray(arrays, samplingRate = 44100, frameDuration=0.1):

    #todo: specify zmin, zmax (for colors)
    extent = [0, (frameDuration / 2) * len(arrays[0]),float(samplingRate) / float(2000), 0] # [xmin, xmax, ymin, ymax]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.imshow(arrays, cmap="nipy_spectral", extent=extent, aspect="auto") #todo: Image data can not convert to float. I don't understand this error.
    fig.colorbar(cax)
    
   
    plt.ylabel("frequencies (kHz)")
    plt.xlabel("time (s)")
    plt.show()

    
#frame duration shouldn't be below 0.05s, as the lowest frequency heard is 20Hz. 20Hz is one oscillation each 0.05s. If the frame is shorter, we can't find those frequencies which may help (as we hear them).
def performFFTs(sound, frameDuration=0.1, windowStep=0.05):
    samplingRate = sound[0]
    normalizedSound = sound[1] #/ (2.**15) #divide each point by 2^15 to normalize. 2^15 is because of the encoding of the sound 
    channel0=0
    if len(sound[1].shape) != 1 :
        channel0 = normalizedSound[:,0] #todo: use both entries
    else :
        channel0 = normalizedSound
        
    result = []
    cursor = 0
    frameFrequency = frameDuration * samplingRate
    stepFrequency = windowStep * samplingRate
    while cursor + frameFrequency < len(channel0) : #for each frame
        frame = channel0[cursor: cursor + frameFrequency]
        cursor += stepFrequency
      
        amplitude = np.fft.fft(frame)
        length = len(frame)
        
        #the fourier transform of the tone returned by the fft function contains both magnitude and phase information and is given in a complex representation (i.e. returns complex numbers). 
        #By taking the absolute value of the fourier transform we get the information about the magnitude of the frequency components.
        nUniquePts = ceil((length + 1 ) / 2.0)
        amplitude = amplitude[0:nUniquePts] #Since FFT is symmetric over it's centre, half the values are just enough.
        amplitude = abs(amplitude)
        
        # scale by the number of points so that the magnitude does not depend on the length of the signal or on its sampling frequency  
        amplitude = amplitude / float(length)
        
        #bfsAmplitude = amplitude / 32768 #todo: only ogr 16 bits https://fr.wikipedia.org/wiki/D%C3%A9cibel_pleine_%C3%A9chelle_(dB_FS)
        #amplitude = amplitude ** 2  # square it to get the power spectrum from the amplitude
        

        if length % 2 > 0: # we've got odd number of points fft
            amplitude[1:len(amplitude)] = amplitude[1:len(amplitude)] * 2
        else:
            amplitude[1:len(amplitude) -1] = amplitude[1:len(amplitude) - 1] * 2 # we've got even number of points fft
        
        frequencies = arange(0, nUniquePts, 1.0) * (samplingRate / length); #Frequency (Hz)
        fftFreq = np.fft.fftfreq(len(amplitude), samplingRate/length)
        
#         print frequencies
#         print fftFreq
#         print amplitude
        #result.append(np.array(20*log10(dbfsAmplitude)))
        result.append(np.array(20*log10(amplitude / (2*32768)))) #todo: is it ok to do not use a logarithmic scale ?
        #result.append(np.array(amplitude))
#         result.append({'frequencies': frequencies, 'power' : np.array(10*log10(amplitude))})
        
    return np.array(result)


# test = performFFTs(load("440_sine.wav"), frameDuration=0.1, windowStep = 0.002)
# visualizeArray(np.transpose(test), frameDuration = 0.1)
