'use strict';

console.log(angular.module('melinder'));
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
                            $state.transitionTo('menu');
                        },3000)
                    }

                }

            })
            .state('menu', {
                url: '/menu',
                templateUrl: 'modules/home/view/home.html'

            })

});

