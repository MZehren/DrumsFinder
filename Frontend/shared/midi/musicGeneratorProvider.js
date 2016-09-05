angular.module('midi')
.factory("musicGeneratorProvider", function (midiProvider) {
    //number of semi-tones (approximal) between each harmonique of a note
    //note : an harmonique is all the frequencies composing a note on the guitar or piano
    //the fundamental is of frequencie f, it first harmonique est of frequencie 2f, the second is of frequencie 3f
    this.harmonic = [0,12,19,24]

    //number of semi-tones from the fundamental
    this.scale = {
        major                   : [0,2,4,5,7,9,11,12],
        minorNatural            : [0,2,3,5,7,8,10,12],
        minorHarmonic           : [0,2,3,5,7,8,11,12],
        minorMelodicAscendante  : [0,2,3,5,7,9,11,12],
        minorMelodicDescendante : [0,2,4,5,7,9,10,12]
    }

    //number of semi-tones from the fundamental
    this.chord = {
        majorPerfect : [0,4,7], //this chord is composed of the fundamental, the major tierce and the quinte
        minorPerfect : [0,3,7],
    }

    this.generateRandomMidi = function(scale, tonic){
     

        for(var i = 0; i < 8 ; i++)
            midiProvider.addNote([50 + this.scale.minorNatural[Math.floor(Math.random() * 8)]],250)


        return midiProvider

    }



    return this;



})
