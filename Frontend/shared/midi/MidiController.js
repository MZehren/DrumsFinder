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

    downloadFile('assets/Partitions/test.mid', function(buffer){
    	var midiFile = new MIDIFile(buffer);
    	$scope.$apply(function(){
    		$scope.midiFile = midiFile;
    	})
    	
    })
  
   

})
