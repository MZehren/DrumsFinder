#! ../ENV/bin/python

from modules import midiProxy
from modules import kerasProxy
from modules import audio

#metaData
frameDuration = 0.075
windowStep = 0.075 #no overlap
sequenceLength = 10 #sequences of 10*0.075 = 0.75 s

#load files
# def loadFolder(path):
# 	for root, dirs, files in os.walk("./samples/mididatabase/files.mididatabase.com/rock/metallica"):
# 	    for idx, file in enumerate(files):
# 	        if file.endswith(".mid"):
# 	            print(os.path.join(root, file))
# 	            songs.append(loadMidiDrums(os.path.join(root, file)))
midi = midiProxy.loadMidiDrums("../../Data/samples/tabs/LegionsOfTheSerpent.mid")
wave = audio.load("../../Data/samples/tabs/LegionsOfTheSerpent.wav")
spectrogram, samplingRate = audio.performFFTs(wave, frameDuration=frameDuration, windowStep=windowStep)

#check correctness
# audio.visualizeSpectrogram(spectrogram, midi=midi,  samplingRate=samplingRate)

#loadModem
model = kerasProxy.getLSTMModel(inputShape=(sequenceLength,len(spectrogram[0]["frequencies"])), outputLength=len(midiProxy.emptyEvent))

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
		print "ERROR"
	if(len(y_candidates) == 0):
		y_candidates.append(midiProxy.emptyEvent)

	Y_train.append(y_candidates[0])

model.fit(X_train, Y_train, nb_epoch=5, batch_size=32)
# testModel(model, maxLength)
# 
# if os.path.isfile('LSTMTest.h5'): 
#     model.load_weights('LSTMTest.h5')
# 
# for idx, song in enumerate(songs):
#     trainModel(model, song, maxLength)
#     print str(idx) + " trained"
#     model.save_weights('LSTMTest.h5')
#     testModel(model, maxLength)
