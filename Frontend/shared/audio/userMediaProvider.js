angular.module('audio')
    .factory('userMediaProvider', ['$interval', function userMediaFactory($interval) {
    
    var myThis = this; //I have to use myThis as this is overriden in $itnerval callback function 
    
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
    this.wave
    this.fftBuffer = new Float32Array( fftSize );
    this.tuner = {pitch: undefined, note : undefined}; //I have to encapsulate pitch and note in tuner as myThis.pitch = x change the ref of the var.
    var intervalPromise = null;
    
    function performFft(){
        var step = (fftSize /  myThis.audioContext.sampleRate) * 1000;
        intervalPromise = $interval(
            function(){
                analyser.getFloatTimeDomainData( myThis.fftBuffer );
                myThis.tuner.pitch = autoCorrelate(myThis.fftBuffer,  myThis.audioContext.sampleRate);
                myThis.tuner.note = noteFromPitch( myThis.tuner.pitch);
                // console.log(buf);
            }, step);
    }
    
    function noteFromPitch( frequency ) {
        if(frequency == -1) 
            return;

        var noteStrings = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
        var noteNum = 12 * (Math.log( frequency / 440 )/Math.log(2) );
        var noteIdx = Math.round( noteNum ) + 69;
        return noteStrings[noteIdx%12];
    }

    function frequencyFromNoteNumber( note ) {
        return 440 * Math.pow(2,(note-69)/12);
    }

    function centsOffFromPitch( frequency, note ) {
        return Math.floor( 1200 * Math.log( frequency / frequencyFromNoteNumber( note ))/Math.log(2) );
    }


    function autoCorrelate( buf, sampleRate ) {
        var SIZE = buf.length;
        var MIN_SAMPLES = 4;    // corresponds to an 11kHz signal
        var MAX_SAMPLES = Math.floor(SIZE/2);
        var best_offset = -1;
        var best_correlation = 0;
        var rms = 0;
        var foundGoodCorrelation = false;
        var correlations = new Array(MAX_SAMPLES);

        for (var i=0;i<SIZE;i++) {
            var val = buf[i];
            rms += val*val;
        }
        rms = Math.sqrt(rms/SIZE);
        if (rms<0.01) // not enough signal
            return -1;

        var lastCorrelation=1;
        for (var offset = MIN_SAMPLES; offset < MAX_SAMPLES; offset++) {
            var correlation = 0;

            for (var i=0; i<MAX_SAMPLES; i++) {
                correlation += Math.abs((buf[i])-(buf[i+offset]));
            }
            correlation = 1 - (correlation/MAX_SAMPLES);
            correlations[offset] = correlation; // store it, for the tweaking we need to do below.
            if ((correlation>0.9) && (correlation > lastCorrelation)) {
                foundGoodCorrelation = true;
                if (correlation > best_correlation) {
                    best_correlation = correlation;
                    best_offset = offset;
                }
            } else if (foundGoodCorrelation) {
                // short-circuit - we found a good correlation, then a bad one, so we'd just be seeing copies from here.
                // Now we need to tweak the offset - by interpolating between the values to the left and right of the
                // best offset, and shifting it a bit.  This is complex, and HACKY in this code (happy to take PRs!) -
                // we need to do a curve fit on correlations[] around best_offset in order to better determine precise
                // (anti-aliased) offset.

                // we know best_offset >=1, 
                // since foundGoodCorrelation cannot go to true until the second pass (offset=1), and 
                // we can't drop into this clause until the following pass (else if).
                var shift = (correlations[best_offset+1] - correlations[best_offset-1])/correlations[best_offset];  
                return sampleRate/(best_offset+(8*shift));
            }
            lastCorrelation = correlation;
        }
        if (best_correlation > 0.01) {
            // console.log("f = " + sampleRate/best_offset + "Hz (rms: " + rms + " confidence: " + best_correlation + ")")
            return sampleRate/best_offset;
        }
        return -1;
    //  var best_frequency = sampleRate/best_offset;
    }





    // this.on('$destroy', function() {
    //     $interval.cancel(intervalPromise);
    // });




		return this;

    }]);