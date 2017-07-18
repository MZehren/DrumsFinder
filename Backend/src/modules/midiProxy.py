#from python-midi in vendors
import midi
import fractions





drum_conversion = {
    35:36, # acoustic bass drum -> bass drum (36)
    37:40, 38:40, # 37:side stick, 38: acou snare, 40: electric snare
    43:41, 47:41, 45:41, 50:41, 48:41, # 41 low floor tom, 43 ghigh floor tom  # 45 low tom, 47 low-mid tom # 50 high tom, 48 hi mid tom
    44:46, 42:46,  # 42 closed HH, 44 pedal HH, 46 open hithat
    57:49, # 57 Crash 2, 49 Crash 1
    59:49, 53:49, 55:49, 51:49, # 59 Ride 2, 51 Ride 1, 53 Ride bell, 55 Splash
    52:49, # 52: China cymbal
    
    #midi notes used by the game Phase Shifter
    #the controller doesn't seem to have a precise representation of each drums
    #when the 110 is played, the 98 is played too but should'nt
    #when the 111 is played, the 99 is played too but shouldn't
    #when the 112 is played, the 100 is played too but shouldn't
    #95:?
    96:36, #kick pad
    97:40, #snare pad
    98:46, #hihat pad
    99:49, #right cymbal
    100:49, #left cymbal
    110:41, #alto tom
    111:41, #med tom
    112:41, #floortom 
}
noteToVector = {
    36 : 0,
    40 : 1,
    41 : 2,
    46 : 3,
    49 : 4
}
vectorToNote = {
    0 : 36, 
    1 : 40,
    2 : 41,
    3 : 46,
    4 : 49,
}
noteToFrequency = {
    36 : 100,
    40 : 2000,
    41 : 1000,
    45 : 2000,
    48 : 2000,
    42 : 3000,
    46 : 3000,
    49 : 4000
}
noteToPlotIcon = {
    36 : "bo",
    40 : "bo",
    41 : "ro",
    45 : "ro",
    48 : "ro",
    42 : "gx",
    46 : "go",
    49 : "gs"
}
emptyEvent = [0,0,0,0,0,0]

def getVectorToNote(vector):
    return [vectorToNote[idx] for idx, value in enumerate(vector) if value]

def getTickToSeconds(deltaTicks, partPerBeats, microsecondsPerBeat):
    return float(deltaTicks) / partPerBeats * microsecondsPerBeat / 1000000 #number of tick since last event / part per beats * microseconds per beats

#return dictionnary to track the absolute position of each events in tick and time instead of relative to each other
def getTempoEvent(pattern):
    tempoEvents = []
    tickCursor = 0
    for tempoEvent in pattern[0]:
        tickCursor += tempoEvent.tick
        if tempoEvent.name == 'Set Tempo':
            currentMpqn = tempoEvent.mpqn
            tempoEvents.append((tickCursor, currentMpqn))
    return tempoEvents

#returns an array of vectors which are the drum played for each midi events in the music
def loadMidiDrums(path):  
    pattern = midi.read_midifile(path)
    if pattern.format != 1 and pattern.resolution < 0:
        print "ERROR midi format not implemented"

    tempoEvents = getTempoEvent(pattern)

    for track in pattern[1:]:
        tickCursor = 0
        timeCursor = 0
        tempoIdx = -1
        currentMpqn = 500000 # default microseconds/beats, which is 120 bpm

        for event in track:
            tickCursor += event.tick #compute the absolute tick number since beginning

            #if there was a previous tempo change
            if len(tempoEvents) > tempoIdx + 1 and tempoEvents[tempoIdx + 1][0] < tickCursor:
                tempoIdx += 1

                #we don't compute if all the tick here have the same value, or if a tempo event occured between them
                if tickCursor - event.tick != tempoEvents[tempoIdx][0]:
                    print "ERROR: tempo event occured between two drums event and not during one."
                    oldSpeedTicks = tempoEvents[tempoIdx][0] - (tickCursor - event.tick)
                    timeCursor += getTickToSeconds(oldSpeedTicks, pattern.resolution, currentMpqn)
                    event.tick = event.tick - oldSpeedTicks # reduce the delta time since the last event as it should be the tempo change

                currentMpqn = tempoEvents[tempoIdx][1]

            #we compute the time is miliseconds since last event
            timeCursor += getTickToSeconds(event.tick, pattern.resolution, currentMpqn) 
            event.tick = timeCursor #todo: assign a new var
        
    tracks = [[event for event in track if isinstance(event, midi.NoteOnEvent) and event.data[1] != 0 ] for track in pattern] # and event.channel == 9

    drumTracks = []
    for idx, track in enumerate(tracks):
        if len(track):
            drumTracks.append(track)
        
    if len(drumTracks) != 1 :
        print "ERROR not enough or too much drumtracks : ", len(drumTracks) 
        return
    
    drumsEvents = drumTracks[0]
    
    if len(drumsEvents) == 0:
        print "no percussion"
        return
    

    timedEvents = {};

    
    for event in drumsEvents:
        event.numberNote = drum_conversion[event.data[0]] if event.data[0] in drum_conversion else event.data[0]
   
        if event.tick not in timedEvents:
            timedEvents[event.tick] = []
        
        if event.numberNote in noteToVector : 
            timedEvents[event.tick].append(noteToVector[event.numberNote])
    
    timedEvents = [{"startTime":time, "notes":[1 if idx in notes else 0 for idx in xrange(len(noteToVector))]} for time, notes in timedEvents.iteritems()]
    return timedEvents
    #get biggest frequency containing every notes
    # frequency = 0;
    # for event in drumsEvents:
    #     frequency = fractions.gcd(frequency, event.tick)
    
    # if frequency < 1:
    #     print "frequency doesn't seem right"
    #     return 
    
    # return [timedEvents[time] if time in timedEvents else [0 for i in range(9)] for time in range(0, max(timedEvents.keys()), frequency)]
    

