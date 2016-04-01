﻿angular.module('nnApp', ['ngRoute', 'home',  'midi', 'audio', 'ui.bootstrap']) 
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'components/home/homeTemplate.html'
        })
        .when('/testMidi', {
            templateUrl: 'shared/midi/testTemplate.html'
        })
        .when('/testSpectrogram', {
            controller : function ($scope, userMediaProvider) {
                userMediaProvider.toggleLiveInput();
                $scope.fftBuffer = userMediaProvider.fftBuffer;
                

            },
            template: '<div class="container-fluid">  <spectrogram-directive slice="fftBuffer" style="width: 200px; height: 200px"></spectrogram-directive> </div>',
        })
        .otherwise({
            redirectTo: '/'
        });
}])


