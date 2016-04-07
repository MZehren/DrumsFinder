angular.module('midi')
.factory("midiProvider", function ($http, $interval, $timeout) {
    var myThis = this;
// // https://github.com/nfroidure/MIDIFile
 //    var myThis = this;
	// // File handlers
	// function readFile(input) {
	// 	var reader = new FileReader();
	// 	reader.readAsArrayBuffer(input.files[0]);
	// 	reader.onloadend = function(event) {
	// 		playFile(event.target.result);
 //   		}
 //   	}

 //    this.downloadFile = function(input, callBack) {
	// 	if(!input)
	// 		return;
	// 	var oReq = new XMLHttpRequest();
	// 	oReq.open("GET", input, true);
	// 	oReq.responseType = "arraybuffer";
	// 	oReq.onload = function (oEvent) {
 //            var buffer = oEvent.currentTarget.response;
 //            var midiFile = new MIDIFile(buffer);
	// 		callBack(midiFile);
	// 	};
	// 	oReq.send(null);
 //   	}
   	// this.getMidiNotesEvents = function (midi){
   	// 	
	   //  var eventsChunk = midi.getMidiEvents();
    //     //creating starting and ending time for each events.
    //     var events = [];
    //     var eventsLookup = {};
    //     eventsChunk.forEach(function(event){
    //         if(event.type != MIDIEvents.EVENT_MIDI_NOTE_ON && event.type != MIDIEvents.EVENT_MIDI_NOTE_OFF) return;

    //         if(event.param1 in eventsLookup && eventsLookup[event.param1]){
    //         	if(event.type != MIDIEvents.EVENT_MIDI_NOTE_OFF)
    //         		console.error("error !")

    //         	var startEvent = eventsLookup[event.param1]
    //         	var stopEvent = event

    //         	startEvent.stopTime = stopEvent.playTime
    //             events.push(startEvent);
    //             eventsLookup[event.param1] = undefined;
    //         }
    //         else{
    //             eventsLookup[event.param1] = event;
    //         }
    //     });

    //     return events;
   	// }


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

    //todo: handle multiple voice event (synchronous notes)
    this.getMidiNotesEvents = function (midiPlayer){

        var eventsChunk = midiPlayer.data;
        //creating starting and ending time for each events.
        var events = [];
        var eventsLookup = {};
        var cursor = 0;
        eventsChunk.forEach(function(data){
            var event = data[0].event;
            cursor += event.deltaTime;
            event.startTime = cursor;
            if(event.subtype != "noteOn" && event.subtype != "noteOff") return;

            if(event.noteNumber in eventsLookup && eventsLookup[event.noteNumber]){
               if(event.subtype != "noteOff")
                   console.error("error !")

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

        return events;
    }

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

    this.noteNumber={
        40 : "a/4",
        41 : "a/4",
        42 : "a/4",
        43 : "a/4",
        44 : "a/4",
        45 : "a/4",
        46 : "a/4", 
        47 : "a/4",
        48 : "a/4",
        49 : "a/4",
        50 : "a/4",
        51 : "a/4",
        52 : "a/4",
        53 : "a/4",
        54 : "a/4",
        55 : "a/4",
        56 : "a/4",
        57 : "a/4",
        58 : "a/4",
        59 : "a/4",
        60 : "a/4",
        61 : "a/4",
        62 : "a/4",
        63 : "a/4",
        64 : "a/4",
        65 : "a/4",
        66 : "a/4",
        67 : "a/4",
        68 : "a/4",
        69 : "a/4",
        70 : "a/4",
        71 : "a/4",
        72 : "a/4",

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
    function noteNumberToKey(note){
        var result = myThis.noteNumber[note.noteNumber];
        if(!result){
            console.log("noteNumberToKey error");
            debugger;
        }
        return result
    }

    this.getMidiSheetMusic = function(midiPlayer){ //has to return with multiple voice, and botes at the good position
        var BPM = midiPlayer.BPM
        var notes = this.getMidiNotesEvents(midiPlayer)
        var tempo = midiPlayer.data.filter(function(d){return d[0].event.subtype == "setTempo"});
        var timeSignature = midiPlayer.data.filter(function(d){return d[0].event.subtype == "timeSignature"})


        var sheet = [];
        var bar = [];
        var barDuration = 0;
        notes.forEach(function(note){
            var noteDuration = noteBeatDuration(note, timeSignature, tempo);
            var noteKey  = noteNumberToKey(note);
            var noteName = noteBeatName(noteDuration);


            barDuration += noteDuration
            if(barDuration == 4){
                bar.push({keys :  [noteKey], duration: noteName})
                sheet.push(bar.slice(0))
                bar = []
                barDuration = 0;
            }
            else if (barDuration > 4){    

                var remainingTime = 4 - (barDuration - noteDuration);
                var remainingNote = noteBeatName(remainingTime);

                bar.push({ keys: ["b/4"], duration: remainingNote+"r" });
                sheet.push(bar.slice(0));
                bar = [{keys : [noteKey], duration: noteName}];
                barDuration = 0;
            }
            else{
                bar.push({keys : [noteKey], duration: noteName});
            }
            

        });    

        return sheet.slice(0,2);



    }




    
    this.playMidiNote = function(note){

        // play the note
        MIDI.noteOn(0, note.noteNumber, note.velocity, 0);
        MIDI.noteOff(0, note.noteNumber, (note.stopTime - note.deltaTime) /1000);
    }



    return this;



})
