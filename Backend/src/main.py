from modules import midiProxy
from modules import kerasProxy

songs = []
# for root, dirs, files in os.walk("./samples/mididatabase/files.mididatabase.com/rock/metallica"):
#     for idx, file in enumerate(files):
#         if file.endswith(".mid"):
#             print(os.path.join(root, file))
#             songs.append(loadMidiDrums(os.path.join(root, file)))
songs.append(midiProxy.loadMidiDrums("../Data/samples/tabs/LegionsOfTheSerpantTrunk.mid"))

maxLength = 40
# numFeatures = len(songs[0][0]) if songs else 9
# model = getLSTMModel(maxLength, numFeatures)
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
