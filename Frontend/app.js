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

                midiProvider.loadMidiFile('assets/Partitions/test.mid', function(){
                    $scope.$apply(function(){

                        $scope.notes = midiProvider.getMidiNotesEvents();
                        console.log($scope.notes);  

                        $scope.sheetMusic = midiProvider.getMidiSheetMusic();
                        console.log($scope.sheetMusic);  
                        
                        $scope.playNote = function(note){
                            midiProvider.playMidiNote(note);
                        }
                        
                        $scope.midi = midiProvider;
                        
                    });

                });

            },
            template: '<button ng-click="midi.playPause()">{{midi.playing ? "pause" : "play"}}</button>' + 
                      '<midi-partition-directive notes="sheetMusic" play-note="playNote" midi="midi" style="width: 100%; height:100%"></midi-partition-directive>' +
                      '<midi-piano-roll-directive notes="notes" play-note="playNote" style="width: 100%; height:100%"></midi-piano-roll-directive>',
        })
        .when('/generateMidi', {
            controller : function ($scope, musicGeneratorProvider) {

                $scope.midi = musicGeneratorProvider.generateRandomMidi(0,0);

                $scope.notes =  $scope.midi.getMidiNotesEvents();
                console.log($scope.notes);  

                $scope.sheetMusic =  $scope.midi.getMidiSheetMusic();
                console.log($scope.sheetMusic);  

                    
            },
            template: '<button ng-click="midi.playPause()">{{midi.playing ? "pause" : "play"}}</button>' + 
                      '{{sheetMusic}}' +
                      '<midi-partition-directive notes="sheetMusic" style="width: 100%; height:100%"></midi-partition-directive>' +
                      '<midi-piano-roll-directive notes="notes" play-note="playNote" style="width: 100%; height:100%"></midi-piano-roll-directive>',
        })
        .otherwise({
            redirectTo: '/'
        });
}])


