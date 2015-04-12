'use strict';

console.log(angular.module('melinder'));
angular.module('melinder')
    .config(function($stateProvider) {

        $stateProvider

            .state('home', {
                url: '/',
                templateUrl: 'modules/home/view/home.html',
                resolve:{
                    userLogged:['userService',function(userService){
                        return userService.getUserLoggued();
                    }]
                }

            })

});

