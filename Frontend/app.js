﻿angular.module('nnApp', ['ngRoute', 'midi', 'ui.bootstrap']) 
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'shared/midi/testTemplate.html'
        })
        .otherwise({
            redirectTo: '/'
        });
}])
