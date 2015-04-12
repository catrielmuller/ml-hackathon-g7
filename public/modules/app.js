'use strict';
var API_DOMAIN = 'https://ml-hackathon-g7.herokuapp.com';

var venderLibs = ['ui.router', 'ionic','ionic.contrib.ui.tinderCards'];

var app = angular.module('melinder', venderLibs);

app.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    });

app.run(function($interval,$http, $rootScope){

    $rootScope.notifications = [];

    $interval(function(){
        if(window.user.id && window.user.preferences && window.user.preferences.length){
            $http.GET(API_DOMAIN + '/api/offer').then(function(data){
                $rootScope.notifications =  data.data;
            })
        }
    }, 30000);

});