'use strict';

var venderLibs = ['ui.router'];

var app = angular.module('melinder', venderLibs);

app.config(function($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/home');

        $stateProvider

            // HOME STATES AND NESTED VIEWS ========================================
            .state('home', {
                url: '/home',
                templateUrl: 'modules/home/view/home.html'
                //template: '<div>partial-home.html</div>,<div>partial-home.html</div>,<div>partial-home.html</div>,<div>partial-home.html</div>'
            })

            // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
            .state('about', {
                // we'll get to this in a bit
            });

    });
