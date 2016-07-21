#from python-midi in vendors
import midi
import fractions

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
vectorToNote = {
    0 : 36, 
    1 : 40,
    2 : 41,
    3 : 45,
    4 : 48,
    5 : 42,
    6 : 46,
    7 : 49,
    8 : 51
}
noteToFrequency = {
    36 : 100,
    40 : 2000,
    41 : 1000,
    45 : 2000,
    48 : 2000,
    42 : 3000,
    46 : 3000,
    49 : 4000,
    51 : 6000
}
noteToPlotIcon = {
    36 : "bo",
    40 : "bo",
    41 : "ro",
    45 : "ro",
    48 : "ro",
    42 : "gx",
    46 : "go",
    49 : "gs",
    51 : "g^"
}

#returns an array of vectors wich are the drum played for each window in the music
def loadMidiDrums(path):  
    pattern = midi.read_midifile(path)
    if pattern.format != 1 and pattern.resolution < 0:
        print "ERROR midi format not implemented"

    #dictionnary to track the absolute position of each events in tick and time instead of relative to each other
    tempoEvents = []
    tickCursor = 0
    for tempoEvent in pattern[0]:
        tickCursor += tempoEvent.tick
        if tempoEvent.name == 'Set Tempo':
            currentMpqn = tempoEvent.mpqn
        tempoEvents.append((tickCursor, currentMpqn))

    for track in pattern[1:]:
        tickCursor = 0
        timeCursor = 0
        tempoIdx = 0
        currentMpqn = 500000 # defaut microseconds/beats, wich is 120 bpm

        for event in track:
            tickCursor += event.tick #compute the absolute tick number since beginning

            #if there was a previous tempo change
            if len(tempoEvents) > tempoIdx + 1 and tempoEvents[tempoIdx + 1][0] < tickCursor:
                currentMpqn = tempoEvents[tempoIdx + 1][1]
                tempoIdx += 1

                #TODO: we don't compute if all the tick here have the same value, or if a tempo event occured between them
                if tickCursor - event.tick != tempoEvents[tempoIdx][0]:
                    print "ERROR: tempo event occured between two drums event and not during one."

            #we compute the time is miliseconds since last event
            timeCursor += float(event.tick) / pattern.resolution * currentMpqn #number of tick since last event / part per beats * microseconds per beats
            event.tick = timeCursor #todo: assign a new var
        
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
    

    timedEvents = {};

    
    for event in drumsEvents:
        event.numberNote = drum_conversion[event.data[0]] if event.data[0] in drum_conversion else event.data[0]
   
        if event.tick not in timedEvents:
            timedEvents[event.tick] = []
        
        if event.numberNote in noteToVector : 
            timedEvents[event.tick].append(noteToVector[event.numberNote])
    
    timedEvents = [(time, [1 if idx in notes else 0 for idx in xrange(9)]) for time, notes in timedEvents.iteritems()]
    return timedEvents
    #get biggest frequency containing every notes
    # frequency = 0;
    # for event in drumsEvents:
    #     frequency = fractions.gcd(frequency, event.tick)
    
    # if frequency < 1:
    #     print "frequency doesn't seem right"
    #     return 
    
    # return [timedEvents[time] if time in timedEvents else [0 for i in range(9)] for time in range(0, max(timedEvents.keys()), frequency)]
    

