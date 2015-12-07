import os

from shared import fft
from shared import midi


wavPath = "./samples/tabs/LegionsOfTheSerpant.wav"
midPath = "./samples/tabs/LegionsOfTheSerpantTrunk.mid"

midiFile = midi.MidiFile()
midiFile.open(midPath)
midiFile.read()
midiFile.close()

events = midiFile.getEvents()


rate, waveFile = fft.load(wavPath)

#lowest frequency = 10Hz = 0.1s per wave
#time between 16th notes : 200bpm = 300 b/ms = 0.3 b/s = 0.075 16th/s
step = 0.075
# step = 0.3
preDelay = 0.02
for time in events:  
    print events[time]
    directory = "./samples/tabs/test/" + str([event.pitch for event in events[time]])
    if not os.path.exists(directory):
        os.makedirs(directory)
    fft.write(directory + "/" + str(time) + ".wav", rate, waveFile[rate * (time - preDelay) : rate * (time + step - preDelay) ])