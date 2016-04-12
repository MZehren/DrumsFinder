﻿angular.module('nnApp', ['ngRoute', 'home',  'midi', 'audio', 'ui.bootstrap']) 
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'components/home/homeTemplate.html'
        })
        .when('/testSpectrogram', {
            controller : function ($scope, userMediaProvider) {
                userMediaProvider.toggleLiveInput();
                $scope.signal = userMediaProvider.signal;
                $scope.tuner = userMediaProvider.tuner;
            },
            template: '<div class="container-fluid">  <spectrogram-directive slice="signal.fftBuffer" style="display:block;"></spectrogram-directive>  {{tuner.pitch}} <br/> {{tuner.note}}</div>',
        })
        .when('/testMidi', {
            controller : function ($scope, midiProvider) {

                midiProvider.loadMidiFile('assets/Partitions/test.mid', function(midi){
                    $scope.$apply(function(){
                        $scope.midi = midi;
                        console.log($scope.midi);

                        $scope.notes = midiProvider.getMidiNotesEvents($scope.midi);
                        console.log($scope.notes);  

                        $scope.sheetMusic = midiProvider.getMidiSheetMusic($scope.midi);
                        console.log($scope.sheetMusic);  
                        
                        console.log($scope.midi.getFileInstruments());
                        
                        $scope.playNote = function(note){
                            midiProvider.playMidiNote(note);
                        }
                        
                        $scope.playPause = function(){
                            if($scope.midi.playing)
                                $scope.midi.stop(function(success){});
                            else
                                $scope.midi.start(function(success){});
                        }
                        
                        $scope.midi.addListener(function(note){
                            $scope.cursor=note;
                        })
                        
                    });

                });

            },
            template: '<button ng-click="playPause()">{{midi.playing ? "pause" : "play"}}</button>' + 
                      '<midi-partition-directive notes="sheetMusic" play-note="playNote" midi="midi" style="width: 100%; height:100%"></midi-partition-directive>' +
                      '<midi-piano-roll-directive notes="notes" play-note="play" style="width: 100%; height:100%"></midi-piano-roll-directive>',
        })
        .otherwise({
            redirectTo: '/'
        });
}])


