angular.module('audio')
    .factory('userMediaProvider', ['$interval', function userMediaFactory($interval) {
    
    var myThis = this;
    
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
            navigator.getUserMedia(dictionary, callback, function(e){alert(e.name);});
        } catch (e) {
            alert('getUserMedia threw exception :' + e);
        }
    }
    

    this.audioContext = new AudioContext();
    var fftSize = 2048;
    function gotStream(stream) {
        // Create an AudioNode from the stream.
        mediaStreamSource =  myThis.audioContext.createMediaStreamSource(stream);
        
        // Connect it to the destination.
        analyser =  myThis.audioContext.createAnalyser();
        analyser.fftSize = fftSize;
        mediaStreamSource.connect( analyser );
        
        performFft();
    }
    
    //todo: use broadcast instead of the watch ?
    //todo: when hitting a breakpoint after the first analyser make the recording to stop..
    this.fftBuffer = new Float32Array( fftSize );
    var intervalPromise = null;
    
    function performFft(){
        var step = (fftSize /  myThis.audioContext.sampleRate) * 1000;
        intervalPromise = $interval(
            function(){
                analyser.getFloatTimeDomainData( myThis.fftBuffer );
                // console.log(buf);
            }, step);
    }
    
    // this.on('$destroy', function() {
    //     $interval.cancel(intervalPromise);
    // });

//     Spectrogram.prototype.getFrequencyValue = function(freq) {
//     var nyquist = this.context.sampleRate/2;
//     var index = Math.round(freq/nyquist * this.freqs.length);
//     return this.freqs[index];
//     }
// 
//     Spectrogram.prototype.getBinFrequency = function(index) {
//     var nyquist = this.context.sampleRate/2;
//     var freq = index / this.freqs.length * nyquist;
//     return freq;
//     }


		return this;

    }]);