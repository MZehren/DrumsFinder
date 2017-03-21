#Open a midi file and a wav and output labelled window of the wave (need to be maintained with the new python midi
import os
import numpy as np 

from modules import audio
from modules import midiProxy

def writeSamples(midiPath, audioPath, outputPath):
    midi = midiProxy.loadMidiDrums(midiPath)
    audioLoad = audio.load(audioPath)
    wave = audioLoad[1]
    rate = audioLoad[0]
    #spectrogram, samplingRate = audio.performFFTs(audioLoad)

    #check correctness
    #audio.visualizeSpectrogram(wave=None, spectrogram=spectrogram, midi=midi)

    #lowest frequency = 10Hz = 0.1s per wave
    #time between 16th notes : 200bpm = 300 b/ms = 0.3 b/s = 0.075 16th/s
    step = 0.5
    # step = 1
     
    
    samples = int(step * rate)
    preDelay = 0.05
     
    #fade in and fade out mask to remove 'pop' which may create aliasing in fft ?
    fade = 0.005
    fadeSamples = int(fade*rate)
    # fadeMask = [i/float(fadeSamples) for i in xrange(int(fadeSamples))] + [1 for i in xrange(int(samples - 2*fadeSamples))] + [1 - i/float(fadeSamples) for i in xrange(int(fadeSamples))]
     
#     features = midi.IncrementDict()
#     print midi
    for midiEvent in midi:  
        #get the name and the time of the midi event
        eventName = midiEvent['notes'] #midiProxy.getVectorToNote(midiEvent['notes']) #from [0,0,1,0...] to [40, 36]
        time = midiEvent["startTime"]
        
        
        #if the event is not in the wave
        min = int(rate * (time - preDelay))
        max = int(rate * (time - preDelay)) + samples
        if min < 0 or max > len(wave):
            continue
        
        
        #create folder for the samples
        directory = outputPath + "/" + str(eventName)
        if not os.path.exists(directory):
            os.makedirs(directory)

         
        # fadein and fadeout to prevent aliasing in the fft ?
        # fadedWave = np.array([[int(wave[min+i][0] * fadeMask[i]), int(wave[min+i][1] * fadeMask[i])] for i in xrange(samples)], dtype = wave.dtype)
     
        #write the isolated wave from the sample
        audio.write(directory + "/" + audioPath[-20:][:-4] + str(time) + ".wav", rate, wave[min:max])
#         audio.write(directory + "/" + str(time) + "f.wav", rate, fadedWave)
        
        print directory + "/" + audioPath[-20:][:-4] + str(time) + ".wav"
   

outputPath = "../../Data/samples/testAtlantis"

for root, dirs, files in os.walk("../../Data/handmade/"):
    for idx, file in enumerate(files):
        if file.endswith(".wav"):
            path = (os.path.join(root, file))
            writeSamples(path[:-3]+"mid", path, outputPath)

        
# writeSamples(midPath, wavPath, outputPath)
print "Done !"
# midiFile = midi.MidiFile()
# midiFile.open(midPath)
# midiFile.read()
# midiFile.close()
# 
# events = midiFile.getEvents()
# 
# 
# rate, waveFile = audio.load(wavPath)
# 
#      features.add(str([event.pitch for event in events[time]]),  fadedWave)
#      
#     for feature in features.dict:
#         wave = np.mean(features.dict[feature][0], axis=1)
#         fft.write("./samples/tabs/test/mono.wav",rate , wave)

