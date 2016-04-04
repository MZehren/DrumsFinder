angular.module('midi')
    .factory("midiProvider", function ($http, $interval, $timeout) {

	// File handlers
	function readFile(input) {
		var reader = new FileReader();
		reader.readAsArrayBuffer(input.files[0]);
		reader.onloadend = function(event) {
			playFile(event.target.result);
   		}
   	}

    this.downloadFile = function(input, callBack) {
		if(!input)
			return;
		var oReq = new XMLHttpRequest();
		oReq.open("GET", input, true);
		oReq.responseType = "arraybuffer";
		oReq.onload = function (oEvent) {
            var buffer = oEvent.currentTarget.response;
            var midiFile = new MIDIFile(buffer);
			callBack(midiFile);
		};
		oReq.send(null);
   	}


   	this.getMidiNotes = function (midi){
   		// https://github.com/nfroidure/MIDIFile
	    var eventsChunk = midi.getMidiEvents();

        //creating starting and ending time for each events.
        var events = [];
        var eventsLookup = {};
        eventsChunk.forEach(function(event){
            if(event.type != MIDIEvents.EVENT_MIDI_NOTE_ON && event.type != MIDIEvents.EVENT_MIDI_NOTE_OFF) return;
            
            if(event.param1 in eventsLookup && eventsLookup[event.param1]){
            	if(event.type != MIDIEvents.EVENT_MIDI_NOTE_OFF)
            		console.error("error !")

            	var startEvent = eventsLookup[event.param1]
            	var stopEvent = event

            	startEvent.stopTime = stopEvent.playTime
                events.push(startEvent);
                eventsLookup[event.param1] = undefined;
            }
            else{
                eventsLookup[event.param1] = event;
            }
        });

        return events;
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
    
    this.playMidiNote = function(note){

        // play the note
        MIDI.noteOn(0, note.param1, note.param2, 0);
        MIDI.noteOff(0, note.param1, (note.stopTime - note.playTime) /1000);
    }



    return this;
  
   

})
