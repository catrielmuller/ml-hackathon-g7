'use strict';

var venderLibs = ['ui.router'];

var app = angular.module('melinder', venderLibs);

app.config(function($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/');
    
    });
