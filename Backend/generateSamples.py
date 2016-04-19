#Open a midi file and a wav and output labelled window of the wave (need to be maintained with the new python midi
import os
import numpy as np 

from shared import fft
from shared import midi

wavPath = "./samples/tabs/LegionsOfTheSerpantVoiceLess.wav"
midPath = "./samples/tabs/LegionsOfTheSerpant.mid"

midiFile = midi.MidiFile()
midiFile.open(midPath)
midiFile.read()
midiFile.close()

events = midiFile.getEvents()


rate, waveFile = fft.load(wavPath)

#lowest frequency = 10Hz = 0.1s per wave
#time between 16th notes : 200bpm = 300 b/ms = 0.3 b/s = 0.075 16th/s
step = 0.075
# step = 1

samples = int(step * rate)
preDelay = 0.02

#fade in and fade out mask to remove 'pop' which may create aliasing in fft ?
fade = 0.005
fadeSamples = int(fade*rate)
fadeMask = [i/float(fadeSamples) for i in xrange(int(fadeSamples))] + [1 for i in xrange(int(samples - 2*fadeSamples))] + [1 - i/float(fadeSamples) for i in xrange(int(fadeSamples))]

features = midi.IncrementDict()
for time in events:  
    print events[time]
    directory = "./samples/tabs/test/" + str([event.pitch for event in events[time]])
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    min = int(rate * (time - preDelay))
    max = int(rate * (time - preDelay)) + samples
    
    if min < 0 or max > len(waveFile):
        continue
    
#     fadedWave = np.array([[waveFile[min+i][0] * fadeMask[i], waveFile[min+i][1] * fadeMask[i]] for i in xrange(samples)], dtype=float)
    fadedWave = np.array([[int(waveFile[min+i][0] * fadeMask[i]), int(waveFile[min+i][1] * fadeMask[i])] for i in xrange(samples)], dtype = waveFile.dtype)

    fft.write(directory + "/" + str(time) + ".wav", rate, waveFile[min:max])
    fft.write(directory + "/" + str(time) + "f.wav", rate, fadedWave)
    features.add(str([event.pitch for event in events[time]]),  fadedWave)

for feature in features.dict:
    wave = np.mean(features.dict[feature][0], axis=1)
#     fft.write("./samples/tabs/test/mono.wav",rate , wave)
