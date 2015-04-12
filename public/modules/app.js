'use strict';
var API_DOMAIN = 'https://ml-hackathon-g7.herokuapp.com';

var venderLibs = ['ui.router', 'ionic','ionic.contrib.ui.tinderCards'];

var app = angular.module('melinder', venderLibs);

app.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    });

