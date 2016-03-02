angular.module('midi')
    .controller("MidiController", function ($scope, $http, $interval, $timeout) {

	// File handlers
	function readFile(input) {
		var reader = new FileReader();
		reader.readAsArrayBuffer(input.files[0]);
		reader.onloadend = function(event) {
			playFile(event.target.result);
   		}
   	}

    function downloadFile(input, callBack) {
		if(!input)
			return;
		var oReq = new XMLHttpRequest();
		oReq.open("GET", input, true);
		oReq.responseType = "arraybuffer";
		oReq.onload = function (oEvent) {
			callBack(oEvent.currentTarget.response);
		};
		oReq.send(null);
   	}

   	//todo: put this in a module ?
   	$scope.getMidiNotes = function (midi){
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

    downloadFile('assets/Partitions/LegionsOfTheSerpant.mid', function(buffer){
    	var midiFile = new MIDIFile(buffer);
    	$scope.$apply(function(){
    		$scope.midiFile = midiFile;
    	})
    	
    })
  
   

})
