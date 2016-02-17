﻿angular.module('nnApp', ['ngRoute', 'home',  'midi', 'audio', 'ui.bootstrap']) 
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'components/home/homeTemplate.html'
        })
        .when('/testMidi', {
            templateUrl: 'shared/midi/testTemplate.html'
        })
        .otherwise({
            redirectTo: '/'
        });
}])
