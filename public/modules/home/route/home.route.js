'use strict';

angular.module('melinder')
    .config(function($stateProvider, $urlRouterProvider) {

        $stateProvider

            .state('home', {
                url: '/',
                templateUrl: 'modules/home/view/home.html'
            })

});

