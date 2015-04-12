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
                    intro :['$timeout','$state', 'Session','userService',function($timeout, $state,Session,userService){
                        var redir = 'user.menu';
                        userService.getUserLoggued(function (user) {
                            console.log(user);
                            if (!user.data.preferences || !user.data.preferences.length) {
                                redir = 'user.category';
                            }
                            $timeout(function(){
                                $state.transitionTo(redir);
                            },3000);
                        });

                    }]

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

            .state('user.category', {
                url: '/category',
                templateUrl: 'modules/home/view/category.html',
                controller:'categoryController'
            });

    });

