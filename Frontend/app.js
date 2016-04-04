﻿angular.module('nnApp', ['ngRoute', 'home',  'midi', 'audio', 'ui.bootstrap']) 
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'components/home/homeTemplate.html'
        })
        .when('/testSpectrogram', {
            controller : function ($scope, userMediaProvider) {
                userMediaProvider.toggleLiveInput();
                $scope.fftBuffer = userMediaProvider.fftBuffer;
                $scope.tuner = userMediaProvider.tuner;
            },
            template: '<div class="container-fluid">  <spectrogram-directive slice="fftBuffer" style="display:block;"></spectrogram-directive>  {{tuner.pitch}} <br/> {{tuner.note}}</div>',
        })
        .when('/testMidi', {
            controller : function ($scope, midiProvider) {

                midiProvider.downloadFile('assets/Partitions/test.mid', function(midi){

                    $scope.$apply(function(){
                        $scope.midi = midi;
                        console.log($scope.midi);

                        $scope.notes = midiProvider.getMidiNotes($scope.midi);
                        console.log($scope.notes);  

                        $scope.play = function(note){
                            midiProvider.playMidiNote(note);
                        } 
                    });

                });

            },
            template: '<midi-partition-directive notes="notes" play-note="play" style="width: 100%; height:100%"></midi-partition-directive>',
        })
        .otherwise({
            redirectTo: '/'
        });
}])


