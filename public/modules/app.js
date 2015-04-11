'use strict';

var venderLibs = ['ui.router'];

angular.module('melinder', venderLibs)
    .config(function($stateProvider, $urlRouterProvider,$locationProvider ) {

        $urlRouterProvider
            .otherwise('/');

        $locationProvider.html5Mode(true);

        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: "/modules/home/view/home.html"
            })


    })
