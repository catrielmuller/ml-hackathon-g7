'use strict';

var module = angular.module('home' , ['ui.router']);

module.config(function($stateProvider, $urlRouterProvider,$locationProvider ) {
    //
    // For any unmatched url, redirect to /state1
    //
    $urlRouterProvider
        .otherwise('/');

    $locationProvider.html5Mode(true);
    // Now set up the states
    $stateProvider
        .state('home', {
            url: "/home",
            templateUrl: "modules/home/view/home.html"
        })


});