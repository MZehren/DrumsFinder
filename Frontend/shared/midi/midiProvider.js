angular.module('midi')
.factory("midiProvider", function ($http, $interval, $timeout) {

    //----------------- UTILS FUNCTIONS
    var myThis = this;
    // in 4/4 time signature
    this.noteDuration={
        "w"     : 4,
        "h"     : 2,
        "q"     : 1,
        "8"     : 0.5,
        "16"    : 4/16,
        "32"    : 4/32,
        "hd"    : 3,
        "qd"    : 1.5,
        "8d"    : 0.75,
        "16d"   : 6/16,
        "32d"   : 6/32
    }

    this.noteNumberMap={
        "-1" : "b/4"
    }
    var notesNames = [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B" ];
    for(var i = 0; i < 127; i++) {
        var index = i,
            key = notesNames[index % 12],
            octave = ((index / 12) | 0) ; //octave = ((index / 12) | 0) - 1; // MIDI scale starts at octave = -1


        key = key + '/';
        
        key += octave;
        // noteMap[key] = i;
        this.noteNumberMap[i] = key;

    }

    // from 1.002 to "q"
    function noteBeatName (beatDuration, timeSignature){
        var closestIdx = "w";
        var closestDistance = 4;

        for(var idx in myThis.noteDuration){
            var distance = Math.abs(beatDuration - myThis.noteDuration[idx]);

            if(Math.min(distance, closestDistance) == distance){
                closestIdx = idx;
                closestDistance = distance;
            }
        }

        return closestIdx;
    }

    //from {startTime: 90, endTime : 180} to "q"
    function noteBeatDuration(note, timeSignature, tempo){
        var microSecondDuration = (note.stopTime - note.startTime) * 1000;
        var beatDuration = microSecondDuration / tempo[0][0].event.microsecondsPerBeat;

        var beatName = noteBeatName(beatDuration);
        return myThis.noteDuration[beatName];
    }

    //from 45 to "a#/1"
    function noteNumberToKey(noteNumber){
        var result = myThis.noteNumberMap[noteNumber];
        if(!result){
            console.log("noteNumberToKey error");
            debugger;
        }
        return result
    }


    MIDI.loadPlugin({
        soundfontUrl: "vendors/MIDI.js-master/examples/soundfont/",
        instrument: "acoustic_grand_piano",
        onprogress: function(state, progress) {
            console.log(state, progress);
        },
        onsuccess: function() {
            MIDI.setVolume(0, 127);
        }
    });

    this.loadMidiFile = function(url, onSuccess){

        MIDI.Player.loadFile(url,  
            function(midi){
                onSuccess(MIDI.Player);
            },
            function(progress){
            },
            function(error){
                console.log(error);
            });
    }












    //--------------- BEHAVIOR FUNCTIONS ----------------


    //todo: handle multiple voice event (synchronous notes)
    //return array of the form [{noteNumber : [-1 / 127], startTime : absolute, stopTime : absolute, deltaTime : relative to previous note}]
    this.getMidiNotesEvents = function (midiPlayer, addSilence){

        var eventsChunk = jQuery.extend(true, [],midiPlayer.data);
        //creating starting and ending time for each events.
        var events = [];
        var eventsLookup = {};
        var cursor = 0;

        //cluster starting and ending events of the same note
        eventsChunk.forEach(function(data){
            var event = data[0].event;
            cursor += event.deltaTime;
            event.startTime = cursor;
            if(event.subtype != "noteOn" && event.subtype != "noteOff") return;

            if(event.noteNumber in eventsLookup && eventsLookup[event.noteNumber]){
               if(event.subtype != "noteOff")
                   console.error("Midi parsing error ! NoteOn event already occured.")

               var startEvent = eventsLookup[event.noteNumber]
               var stopEvent = event

               startEvent.stopTime = cursor;

               events.push(startEvent);
               eventsLookup[event.noteNumber] = undefined;
            }
            else{
                eventsLookup[event.noteNumber] = event;
            }
        });

        //cluster parallels events
        //todo: I assume that in the same voice parallels notes start and end at the same time !
        eventsLookup = {} //events by starting time
        events.forEach(function(event){
            if(!(event.startTime in eventsLookup))
                eventsLookup[event.startTime] = [];
            eventsLookup[event.startTime].push(event);
        })
        events = []; //transform eventsLookup to array.. dirty I think..
        for(eventIdx in eventsLookup){
            var parallelEvents = eventsLookup[eventIdx];
            parallelEvents[0].noteNumber = parallelEvents.map(function(d){return d.noteNumber});
            events.push(parallelEvents[0])
        }




        //add silence between events if they aren't together
        if(addSilence){
            var lastStopEvent = 0;
            events.forEach(function(event, idx){
                if(lastStopEvent < event.startTime){
                    events.splice(idx, 0, {noteNumber: ["-1"], startTime: lastStopEvent, stopTime: event.startTime});
                }

                lastStopEvent = event.stopTime;
            });
        }

        return events;
    }


    //return array representing the sheet music of the shape bar/notes
    //[[{keys:["a/4"], duration "w"}], ]
    this.getMidiSheetMusic = function(midiPlayer){ //has to return with multiple voice, and botes at the good position
        var BPM = midiPlayer.BPM
        var notes = this.getMidiNotesEvents(midiPlayer, true)
        var tempo = midiPlayer.data.filter(function(d){return d[0].event.subtype == "setTempo"});
        var timeSignature = midiPlayer.data.filter(function(d){return d[0].event.subtype == "timeSignature"})


        var sheet = [];
        var bar = [];
        var barDuration = 0;
        notes.forEach(function(note){
            var noteDuration = noteBeatDuration(note, timeSignature, tempo);
            var noteKey  = note.noteNumber.map(function(d){return noteNumberToKey(d)}); //todo order keys https://github.com/0xfe/vexflow/issues/104
            var noteDurationName = noteBeatName(noteDuration);
            
            if(note.noteNumber[0] == "-1")
                noteDurationName += "r";


            bar.push({keys : noteKey, duration: noteDurationName});
            barDuration += noteDuration
            if(barDuration == 4){
                sheet.push(bar.slice(0))
                bar = []
                barDuration = 0;
            }
            else if (barDuration > 4){    
                console.error("not good bar !")
            }

        });    

        return sheet;



    }




    
    this.playMidiNote = function(note){

        // play the note
        MIDI.noteOn(0, note.noteNumber, note.velocity, 0);
        MIDI.noteOff(0, note.noteNumber, (note.stopTime - note.deltaTime) /1000);
    }



    return this;



})
