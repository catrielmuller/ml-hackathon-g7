'use strict';
var API_DOMAIN = 'http://ml-hackathon-g7.herokuapp.com';

var venderLibs = ['ui.router', 'ionic'];

var app = angular.module('melinder', venderLibs);

app.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    });

