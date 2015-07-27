﻿angular.module('nnApp', ['ngRoute', 'home', 'partition' ]) 
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'app/components/home/homeTemplate.html'
        })
        .otherwise({
            redirectTo: '/'
        });
}])
