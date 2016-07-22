#! ../ENV/bin/python
import sys
import os

from modules import midiProxy
from modules import kerasProxy
from modules import audio

import numpy as np



def loadFolder(path):
    songs = []
    for root, dirs, files in os.walk(path):
        for idx, file in enumerate(files):
            if file.endswith(".mid"):
                print(os.path.join(root, file))
                songs.append(midiProxy.loadMidiDrums(os.path.join(root, file)))

    return songs

def createTrainData(spectrogram, midi, sequenceLength):
    #create training data
    X_train = []
    Y_train = []
    for fftIdx in range(len(spectrogram)):
        if fftIdx + sequenceLength > len(spectrogram):
            break

        X_train.append([spectrogram[i]["frequencies"] for i in range(fftIdx, fftIdx + sequenceLength)])

        y_candidates = []
        for event in midi:
            if event["startTime"] < spectrogram[fftIdx]["stopTime"] and event["startTime"] > spectrogram[fftIdx]["startTime"]:
                y_candidates.append(event["notes"])

        if(len(y_candidates) > 1):
            print "ERROR, this fft is over more than one midi event"
        if(len(y_candidates) == 0):
            y_candidates.append(midiProxy.emptyEvent)
        Y_train.append(y_candidates[0])

    return X_train, Y_train

#metaData



def train(weightsPath, wavPath, midiPath, frameDuration = 0.075, windowStep = 0.075, sequenceLength = 10): #sequences of 10*0.075 = 0.75 s
    midi = midiProxy.loadMidiDrums(midiPath)
    wave = audio.load(wavPath)
    spectrogram, samplingRate = audio.performFFTs(wave, frameDuration=frameDuration, windowStep=windowStep)
    #normalize
    max = np.amax([fft["frequencies"] for fft in spectrogram])
    min = np.amin([fft["frequencies"] for fft in spectrogram])
    for fft in spectrogram:
        fft["frequencies"] = [(value - min) / (max - min) for value in fft["frequencies"]]

    #check correctness
    # audio.visualizeSpectrogram(spectrogram, midi=midi,  samplingRate=samplingRate)

    #loadModem
    model = kerasProxy.getLSTMModel(inputShape=(sequenceLength,len(spectrogram[0]["frequencies"])), outputLength=len(midiProxy.emptyEvent))
    if os.path.isfile(weightsPath):
        print "Weights loaded from : " + weightsPath
        model.load_weights(weightsPath)

    X_train, Y_train = createTrainData(spectrogram, midi, sequenceLength)

    audio.visualizeSpectrogram(spectrogram, midi=test(X_train, model, windowStep),  samplingRate=samplingRate)
    #model.fit(X_train, Y_train, nb_epoch=1, batch_size=256) #epoch = number of time all the test data are used, batch_size= number of training examples in one forward/backward pass (thei higher, the more memory is used)

    audio.visualizeSpectrogram(spectrogram, midi=test(X_train, model, windowStep),  samplingRate=samplingRate)

    model.save_weights(weightsPath,  overwrite=True)

def test(X_test, model, windowStep):
    proba = model.predict_proba(X_test[:500], batch_size=1)

    events = [{"startTime" : i * windowStep, "notes" :  [1 if note > 0.5 else 0 for note in event]} for i, event in enumerate(proba)]
    return events


if len(sys.argv) == 1:
    #print
    #print " usage : " + sys.argv[0] +" weightsPath wavPath midiPath"
    train("LSTMWeights.h5", "../../Data/samples/tabs/LegionsOfTheSerpent.wav", "../../Data/samples/tabs/LegionsOfTheSerpent.mid")