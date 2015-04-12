'use strict';

angular.module('melinder')
    .config(function($stateProvider) {

        $stateProvider

            .state('home', {
                url: '/',
                templateUrl: 'modules/home/view/intro.html',
                resolve:{
                    userLogged:['userService',function(userService){
                        return userService.getUserLoggued();
                    }],
                    intro : function($timeout, $state){
                        $timeout(function(){
                            console.log('me voooy');
                            $state.transitionTo('user.menu');
                        },3000)
                    }

                }

            })
            .state('user', {
                abstract: true,
                templateUrl: 'modules/home/view/header.html',
                resolve: {
                    userLogged: ['userService', function (userService) {
                   //     return userService.getUserLoggued();
                    }]
                }
            })
            .state('user.menu', {
                url: '/menu',
                templateUrl: 'modules/home/view/home.html',
                controller:'homeController'
            })

});

