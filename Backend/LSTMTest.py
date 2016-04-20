import midi
import os
import fractions
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout
import numpy as np

#returns an array of vectors wich are the drum played for each window in the music
def loadMidiDrums(path):  
    pattern = midi.read_midifile(path)
#     TrackProgramChangeEvent = [[event for event in track if isinstance(event, midi.ProgramChangeEvent)] for track in pattern]
#     drumTracks = [track for idx, track in enumerate(pattern) if len(TrackProgramChangeEvent[idx]) and TrackProgramChangeEvent[idx][-1].data == [10]]
    for track in pattern: #todo: setting absolute value for tick. Cause I can't assign new value. so change this behavior !
        absoluteTick = 0
        for event in track:
            absoluteTick += event.tick
            event.tick = absoluteTick
        
    tracks = [[event for event in track if isinstance(event, midi.NoteOnEvent) and event.channel == 9] for track in pattern] 

    drumTracks = []
    for idx, track in enumerate(tracks):
        if len(track):
            drumTracks.append(track)
        
    if len(drumTracks) != 1 :
        print "ERROR not enough or too much drumtracks"
        print len(drumTracks) 
        return
    
    drumsEvents = drumTracks[0]
    
    if len(drumsEvents) == 0:
        print "no percussion"
        return
    
    drum_conversion = {
        35:36, # acoustic bass drum -> bass drum (36)
        37:40, 38:40, # 37:side stick, 38: acou snare, 40: electric snare
        43:41, # 41 low floor tom, 43 ghigh floor tom
        47:45, # 45 low tom, 47 low-mid tom
        50:48, # 50 high tom, 48 hi mid tom
        44:42, # 42 closed HH, 44 pedal HH
        57:49, # 57 Crash 2, 49 Crash 1
        59:51, 53:51, 55:51, # 59 Ride 2, 51 Ride 1, 53 Ride bell, 55 Splash
        52:49 # 52: China cymbal
    }

    timedEvents = {};
    noteToVector = {
        36 : 0,
        40 : 1,
        41 : 2,
        45 : 3,
        48 : 4,
        42 : 5,
        46 : 6,
        49 : 7,
        51 : 8
    }
    
    for event in drumsEvents:
        event.numberNote = drum_conversion[event.data[0]] if event.data[0] in drum_conversion else event.data[0]
   
        if event.tick not in timedEvents:
            timedEvents[event.tick] = []
        
        if event.numberNote in noteToVector : 
            timedEvents[event.tick].append(noteToVector[event.numberNote])
    
    timedEvents = {timeStamp : [1 if idx in notes else 0 for idx in xrange(9)] for timeStamp, notes in timedEvents.iteritems()}
    
    #get biggest frequency containing every notes
    frequency = 0;
    for event in drumsEvents:
        frequency = fractions.gcd(frequency, event.tick)
    
    if frequency < 1:
        print "frequency doesn't seem right"
        return 
    
    return [timedEvents[time] if time in timedEvents else [0 for i in range(9)] for time in range(0, max(timedEvents.keys()), frequency)]
  
def getLSTMModel(maxLength, numFeatures):
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(maxLength, numFeatures)))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(numFeatures))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    
    return model

def trainModel(model, song, maxLength):

    X_train = [[song[i] for i in range(start, start + maxLength) ] for start in range(0, len(song)-maxLength)]
    Y_train = [song[i] for i in range(maxLength, len(song))]
    
    model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)
    
def testModel(model, maxLength):
#         36 : 0,
#         40 : 1,
#         41 : 2,
#         45 : 3,
#         48 : 4,
#         42 : 5,
#         46 : 6,
#         49 : 7,
#         51 : 8
    X_tests = [
        [
            [1,0,0,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,0,1],
        ],
        [
            [1,0,0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
        ]
    ]
    for X_test in X_tests:
        X_test = [X_test[i % len(X_test)] for i in range(maxLength)]
        Y = X_test[maxLength % len(X_test)]
        
        classes = model.predict_classes(np.asarray([X_test]), batch_size=1)
        proba = model.predict_proba(np.asarray([X_test]), batch_size=1)
        
        print X_test
        print Y
        print classes
        print proba
        print


    
    
songs = []
# for root, dirs, files in os.walk("./samples/mididatabase/files.mididatabase.com/rock/metallica"):
#     for idx, file in enumerate(files):
#         if file.endswith(".mid"):
#             print(os.path.join(root, file))
#             songs.append(loadMidiDrums(os.path.join(root, file)))
songs.append(loadMidiDrums("./samples/tabs/LegionsOfTheSerpantTrunk.mid"))
maxLength = 40
numFeatures = len(songs[0][0]) if songs else 9
model = getLSTMModel(maxLength, numFeatures)
testModel(model, maxLength)

if os.path.isfile('LSTMTest.h5'): 
    model.load_weights('LSTMTest.h5')

for idx, song in enumerate(songs):
    trainModel(model, song, maxLength)
    print str(idx) + " trained"
    model.save_weights('LSTMTest.h5')
    testModel(model, maxLength)
