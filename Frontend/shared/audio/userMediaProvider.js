angular.module('audio')
    .factory('userMediaProvider', [function featuresFactory() {

    this.toggleLiveInput = function() {
    getUserMedia(
    	{
            "audio": {
                "mandatory": {
                    "googEchoCancellation": "false",
                    "googAutoGainControl": "false",
                    "googNoiseSuppression": "false",
                    "googHighpassFilter": "false"
                },
                "optional": []
            },
        }, gotStream);
    }




    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    var mediaStreamSource = null;
    var analyser = null;
    function getUserMedia(dictionary, callback) {
        try {
            navigator.getUserMedia = 
                navigator.getUserMedia ||
                navigator.webkitGetUserMedia ||
                navigator.mozGetUserMedia;
            navigator.getUserMedia(dictionary, callback, function(){alert('Stream generation failed.');});
        } catch (e) {
            alert('getUserMedia threw exception :' + e);
        }
    }
    

    var audioContext = new AudioContext();
    var fftSize = 2048;
    function gotStream(stream) {
        // Create an AudioNode from the stream.
        mediaStreamSource = audioContext.createMediaStreamSource(stream);
        
        // Connect it to the destination.
        analyser = audioContext.createAnalyser();
        analyser.fftSize = fftSize;
        mediaStreamSource.connect( analyser );
        
        performFft();
    }
    
    var buf = new Float32Array( fftSize );
    function performFft(){
        analyser.getFloatTimeDomainData( buf );
        console.log(buf);
    }



		return this;

    }]);